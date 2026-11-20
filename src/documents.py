"""Read corpus Markdown and prepare chunks with source metadata and citation positions."""

import hashlib
import json
import re
from datetime import date
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

REQUIRED_FIELDS = ("document_id", "document_type", "title", "version", "effective_from", "status")
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
    """Read YAML metadata separately from original Markdown; allow corpus sources only."""
    if not path.resolve().is_relative_to(corpus_dir.resolve()):
        raise ValueError(f"Source is outside the corpus: {path}")
    if path.suffix != ".md":
        raise ValueError(f"Expected a Markdown source: {path}")

    source = path.read_bytes().decode("utf-8")
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
        metadata[field] = str(value)

    for field in ("effective_from", "effective_to"):
        if field in metadata:
            date.fromisoformat(metadata[field])

    metadata["source_path"] = (Path("corpus") / path.relative_to(corpus_dir)).as_posix()
    metadata["source_checksum"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return metadata, source[frontmatter.end() :]


def _section_ranges(body: str) -> list[tuple[str, int, int]]:
    """Locate numbered headings using Markdown parsing, excluding fenced code headings.

    A section's direct text ends at the next numbered heading. A chunk may
    overlap several such ranges; all those IDs belong in its citation metadata.
    """
    line_starts = [0]
    for line in body.splitlines(keepends=True):
        line_starts.append(line_starts[-1] + len(line))

    headings = []
    tokens = MarkdownIt("commonmark").parse(body)
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        heading = tokens[index + 1].content
        section = re.match(r"^(\d+(?:\.\d+)*)(?:[.)])?(?:\s|$)", heading)
        if section:
            headings.append((section.group(1), line_starts[token.map[0]]))

    ranges = []
    for index, (section_id, start) in enumerate(headings):
        end = headings[index + 1][1] if index + 1 < len(headings) else len(body)
        ranges.append((section_id, start, end))
    return ranges


def prepare_chunks(corpus_dir: Path, chunker) -> list[dict]:
    """Prepare the current recursive baseline with stable IDs and flat source metadata.

    Positions refer to the Markdown body, excluding YAML frontmatter. Introductory
    text before the first numbered heading has no section ID; none is invented.
    """
    corpus_dir = Path(corpus_dir)
    paths = sorted(corpus_dir.rglob("*.md"))
    if not paths:
        raise ValueError(f"No Markdown sources found in {corpus_dir}")

    documents_seen = set()
    records = []
    for path in paths:
        metadata, body = load_document(path, corpus_dir)
        document_id = metadata["document_id"]
        if document_id in documents_seen:
            raise ValueError(f"Duplicate document_id: {document_id}")
        documents_seen.add(document_id)
        section_ranges = _section_ranges(body)

        for chunk in chunker.chunk_with_offsets(body):
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
                "recursive",
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
                    "section_ids": list(dict.fromkeys(section_ids)),
                    "chunk_strategy": "recursive",
                    "chunk_size": chunker.chunk_size,
                    "chunk_overlap": chunker.overlap,
                    "start_char": chunk.start,
                    "end_char": chunk.end,
                }
            )
    return records
