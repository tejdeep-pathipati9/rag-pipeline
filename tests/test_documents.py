"""Check source metadata, stable IDs and citation mappings without external services."""

from unittest.mock import Mock

import pytest
from markdown_it.token import Token

from src.chunking import RecursiveChunker
from src.documents import prepare_chunks


def test_prepared_chunks_include_source_metadata_and_all_overlapping_sections(corpus, tokenizer):
    """A chunk spanning headings carries every source section, without YAML in its text."""
    chunker = RecursiveChunker(tokenizer=tokenizer, chunk_size=100, overlap=0)
    chunks = prepare_chunks(corpus, chunker)

    assert len(chunks) == 1
    record = chunks[0]
    assert record["document_id"] == "TEST-POLICY"
    assert record["document_type"] == "policy"
    assert record["title"] == "Hotel Policy"
    assert record["version"] == "2.0"
    assert record["effective_from"] == "2026-01-01"
    assert record["status"] == "current"
    assert record["source_path"] == "corpus/policy.md"
    assert record["chunk_strategy"] == "recursive"
    assert record["section_ids"] == ["1", "1.1", "2"]
    assert "effective_to" not in record
    assert "document_id:" not in record["body"]
    assert "Never index" not in record["body"]


def test_optional_end_date_is_preserved_without_changing_source_status(corpus, tokenizer):
    """Preserve the original metadata, even when a historical version is marked current."""
    path = corpus / "policy.md"
    path.write_text(
        path.read_text().replace("status: current", "status: current\neffective_to: 2026-12-31")
    )
    record = prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))[0]
    assert record["effective_to"] == "2026-12-31"
    assert record["status"] == "current"


def test_section_mapping_ignores_headings_in_code_and_tracks_repeated_text(corpus, tokenizer):
    """Use source ranges, not string search or headings that merely appear in code."""
    path = corpus / "policy.md"
    header = path.read_text().split("---", 2)[1]
    body = "## 1. First\nsame words\n\n## 2. Second\nsame words\n\n```\n## 99. Fake\n```\n"
    path.write_text(f"---{header}---\n{body}")
    records = prepare_chunks(corpus, RecursiveChunker(tokenizer, 4, 0))

    for record in records:
        assert body[record["start_char"] : record["end_char"]] == record["body"]
        assert "99" not in record["section_ids"]
    repeated = [record for record in records if record["body"] == "same words"]
    assert [record["section_ids"] for record in repeated] == [["1"], ["2"]]


def test_chunk_ids_are_stable_and_allow_metadata_updates(corpus, tokenizer):
    """Reruns reuse IDs; changing status updates the same chunks rather than duplicating them."""
    chunker = RecursiveChunker(tokenizer, 6, 1)
    first = prepare_chunks(corpus, chunker)
    assert first == prepare_chunks(corpus, chunker)
    path = corpus / "policy.md"
    path.write_text(path.read_text().replace("status: current", "status: superseded"))
    changed = prepare_chunks(corpus, chunker)
    assert [record["_id"] for record in first] == [record["_id"] for record in changed]
    assert all(record["status"] == "superseded" for record in changed)


def test_missing_source_metadata_fails_before_indexing(corpus, tokenizer):
    """Incomplete provenance must not be silently replaced with invented values."""
    path = corpus / "policy.md"
    path.write_text(path.read_text().replace("document_id: TEST-POLICY\n", ""))
    with pytest.raises(ValueError, match="document_id"):
        prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))


def test_duplicate_document_ids_are_rejected(corpus, tokenizer):
    """Two files cannot claim the same citation identity."""
    (corpus / "duplicate.md").write_text((corpus / "policy.md").read_text())
    with pytest.raises(ValueError, match="Duplicate document_id"):
        prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))


def test_symlinks_cannot_pull_non_corpus_files_into_index(corpus, tokenizer, tmp_path):
    """The corpus allowlist also applies to the resolved file path."""
    (corpus / "external.md").symlink_to(tmp_path / "evaluation.md")
    with pytest.raises(ValueError, match="outside"):
        prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))


def test_missing_heading_positions_fail_before_citation_mapping(corpus, tokenizer, monkeypatch):
    """A heading without a source range must not silently lose its citation mapping."""
    parser = Mock()
    parser.parse.return_value = [
        Token("heading_open", "h2", 1),
        Token("inline", "", 0, content="1. Eligibility"),
    ]
    monkeypatch.setattr("src.documents.MarkdownIt", lambda *args: parser)

    with pytest.raises(ValueError, match="heading.*source line positions"):
        prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))
