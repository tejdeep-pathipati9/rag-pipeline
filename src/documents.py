"""Prepare source records before embedding or uploading anything.

load_document separates YAML metadata from the original Markdown body.
prepare_chunks adds stable IDs and section mappings to the chunker's text slices.
"""

import hashlib
import json
import re
from datetime import date
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

REQUIRED_FIELDS = ("document_id", "document_type", "title", "version", "effective_from", "status")
# Missing optional fields stay absent. In particular, do not invent a policy end date.
OPTIONAL_FIELDS = (
    "effective_to",
    "case_id",
    "record_type",
    "source_kind",
    "source_url",
    "authority_level",
    "investigation_status",
    "offer_status",
    "primary_cause",
)


def load_document(path: Path, corpus_dir: Path) -> tuple[dict, str]:
    """Return (source_metadata, markdown_body) for one file inside the corpus.

    Metadata is kept out of embedding input. Source values, including the
    intentionally incorrect historical status, are preserved without repairs.
    """
    # Resolve symlinks too, so a corpus entry cannot pull in an outside file.
    if not path.resolve().is_relative_to(corpus_dir.resolve()):
        raise ValueError(f"Source is outside the corpus: {path}")
    if path.suffix != ".md":
        raise ValueError(f"Expected a Markdown source: {path}")

    # Reading bytes preserves original line endings for source-text reconstruction.
    source = path.read_bytes().decode("utf-8")
    # YAML lives between the opening and closing --- lines; the rest is Markdown.
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", source, re.DOTALL)
    if frontmatter is None:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    fields = yaml.safe_load(frontmatter.group(1))
    if not isinstance(fields, dict):
        raise ValueError(f"Expected YAML metadata fields: {path}")

    metadata = {}
    for field in REQUIRED_FIELDS + OPTIONAL_FIELDS:
        value = fields.get(field)
        if value is None or value == "":
            if field in REQUIRED_FIELDS:
                raise ValueError(f"Missing {field}: {path}")
            continue
        if not isinstance(value, (str, int, float, date)) or isinstance(value, bool):
            raise ValueError(f"Expected a scalar {field}: {path}")
        # YAML can load dates and numeric versions as Python objects. Store
        # consistent strings in Pinecone, such as "2026-01-01" and "2.0".
        metadata[field] = str(value)

    for field in ("effective_from", "effective_to"):
        if field in metadata:
            date.fromisoformat(metadata[field])

    # A portable path and file fingerprint let a retrieved chunk be traced to its source.
    metadata["source_path"] = (Path("corpus") / path.relative_to(corpus_dir)).as_posix()
    metadata["source_checksum"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return metadata, source[frontmatter.end() :]


def _section_ranges(body: str) -> list[tuple[str, int, int]]:
    """Locate numbered headings using Markdown parsing, excluding fenced code headings.

    A section's direct text ends at the next numbered heading. A chunk may
    overlap several such ranges; all those IDs belong in its citation metadata.
    """
    # Markdown headings have line numbers; chunks have character positions.
    # This lookup converts the two into the same coordinate system.
    line_starts = [0]
    for line in body.splitlines(keepends=True):
        line_starts.append(line_starts[-1] + len(line))

    headings = []
    tokens = MarkdownIt("commonmark").parse(body)
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        line_range = token.map
        if line_range is None:
            raise ValueError("Markdown heading is missing source line positions.")
        # A heading_open token is followed by the token containing its title.
        heading = tokens[index + 1].content
        # Extract "4" or "4.1" from numbered headings; skip unnumbered titles.
        section = re.match(r"^(\d+(?:\.\d+)*)(?:[.)])?(?:\s|$)", heading)
        if section:
            headings.append((section.group(1), line_starts[line_range[0]]))

    ranges = []
    for index, (section_id, start) in enumerate(headings):
        end = headings[index + 1][1] if index + 1 < len(headings) else len(body)
        ranges.append((section_id, start, end))
    return ranges


def prepare_chunks(corpus_dir: Path, chunker) -> list[dict]:
    """Prepare chunks with stable IDs and flat source metadata.

    Positions refer to the Markdown body, excluding YAML frontmatter. Introductory
    text before the first numbered heading has no section ID; none is invented.
    Returned records contain _id, body and flat metadata. Ingestion adds vectors later.
    """
    corpus_dir = Path(corpus_dir)
    paths = sorted(corpus_dir.rglob("*.md"))
    if not paths:
        raise ValueError(f"No Markdown sources found in {corpus_dir}")

    strategy = chunker.strategy
    documents_seen = set()
    records = []
    for path in paths:
        metadata, body = load_document(path, corpus_dir)
        document_id = metadata["document_id"]
        # A citation combines document_id and section_id, so document IDs must be unique.
        if document_id in documents_seen:
            raise ValueError(f"Duplicate document_id: {document_id}")
        documents_seen.add(document_id)
        section_ranges = _section_ranges(body)

        for chunk in chunker.chunk_with_offsets(body):
            # Include every section whose source range overlaps this chunk.
            # Strict comparisons exclude sections that only touch a chunk's boundary.
            section_ids = [
                section_id
                for section_id, start, end in section_ranges
                if start < chunk.end and chunk.start < end
            ]
            # The same source slice and configuration get the same ID on reruns.
            # Status/date updates stay metadata updates on those existing IDs.
            identity = [
                document_id,
                metadata["version"],
                metadata["source_path"],
                strategy,
                chunker.chunk_size,
                chunker.overlap,
                chunk.start,
                chunk.end,
                chunk.text,
            ]
            digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode()).hexdigest()
            records.append(
                {
                    "_id": digest,
                    "body": chunk.text,
                    **metadata,
                    # Remove duplicate IDs while retaining their order in the source.
                    "section_ids": list(dict.fromkeys(section_ids)),
                    "chunk_strategy": strategy,
                    "chunk_size": chunker.chunk_size,
                    "chunk_overlap": chunker.overlap,
                    "start_char": chunk.start,
                    "end_char": chunk.end,
                }
            )
            if chunk.parent_start is not None and chunk.parent_end is not None:
                start, end = chunk.parent_start, chunk.parent_end
                parent_text = body[start:end]
                parent_identity = [document_id, metadata["version"], start, end, parent_text]
                records[-1].update(
                    {
                        "parent_id": hashlib.sha256(
                            json.dumps(parent_identity, ensure_ascii=False).encode()
                        ).hexdigest(),
                        "parent_body": parent_text,
                        "parent_start_char": start,
                        "parent_end_char": end,
                        "parent_section_ids": [
                            section for section, a, b in section_ranges if a < end and start < b
                        ],
                    }
                )
    return records
