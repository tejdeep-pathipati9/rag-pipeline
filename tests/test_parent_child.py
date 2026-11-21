"""Verify complete policy evidence, original source slices and bounded context."""

from src.chunking import ParentChildChunker
from src.documents import load_document, prepare_chunks
from src.retrieval import assemble_evidence


def test_children_keep_parents_and_recover_uncut_table(corpus, tokenizer):
    path = corpus / "policy.md"
    frontmatter = path.read_text().split("---", 2)[1]
    body = (
        "# Care\n\n## 4. Hotel\n"
        "### 4.1 Conditions\nAn overnight away from home is required.\n\n"
        "### 4.4 Exclusions\n"
        "| Cause | Result |\n| --- | --- |\n| Weather | Excluded |\n| Crew | Included |\n\n"
        "## 5. Review\nRefer unresolved facts to an agent.\n"
    )
    path.write_text(f"---{frontmatter}---\n{body}")
    chunker = ParentChildChunker(tokenizer, 8, 1)
    chunks = prepare_chunks(corpus, chunker)
    selected = next(chunk for chunk in chunks if "4.4" in chunk["section_ids"])
    parent = assemble_evidence([selected], tokenizer)[0]

    assert all(len(tokenizer.encode(chunk["body"])) <= 8 for chunk in chunks)
    assert parent["section_ids"] == ["4", "4.1", "4.4"]
    assert "An overnight away from home is required." in parent["body"]
    assert "| Cause | Result |" in parent["body"]
    assert "| Crew | Included |" in parent["body"]
    assert "## 5." not in parent["body"]
    assert parent["child_id"] == selected["_id"]
    for record in [*chunks, parent]:
        assert body[record["start_char"] : record["end_char"]] == record["body"]
    assert chunks == prepare_chunks(corpus, chunker)


def test_expansion_deduplicates_parents_and_enforces_token_budget(corpus, tokenizer):
    chunks = prepare_chunks(corpus, ParentChildChunker(tokenizer, 4, 1))
    children = [chunk for chunk in chunks if "parent_id" in chunk]
    first = next(chunk for chunk in children if "1.1" in chunk["parent_section_ids"])
    sibling = next(
        chunk
        for chunk in children
        if chunk["parent_id"] == first["parent_id"] and chunk["_id"] != first["_id"]
    )
    other = next(chunk for chunk in children if chunk["parent_id"] != first["parent_id"])
    budget = len(tokenizer.encode(first["parent_body"]))
    evidence = assemble_evidence([first, sibling, other], tokenizer, token_budget=budget)

    assert len(evidence) == 1
    assert evidence[0]["_id"] == first["parent_id"]
    assert "child_id" not in first  # Do not mutate the ranked search hits.
    assert sum(len(tokenizer.encode(hit["body"])) for hit in evidence) <= budget


def test_heading_at_start_and_fenced_headings_are_handled(tokenizer):
    text = "## 1. Hotel\nFirst condition.\n\n```\n## 99. Not a section\n```\nLast condition.\n"
    chunks = ParentChildChunker(tokenizer, 6, 1).chunk_with_offsets(text)
    assert len(chunks) > 1
    assert all(chunk.parent_start == 0 and chunk.parent_end == len(text) for chunk in chunks)


def test_policy_metadata_repair_reuses_child_and_parent_ids(corpus, tokenizer):
    chunker = ParentChildChunker(tokenizer, 6, 1)
    before = prepare_chunks(corpus, chunker)
    path = corpus / "policy.md"
    path.write_text(path.read_text().replace("status: current", "status: superseded"))
    after = prepare_chunks(corpus, chunker)
    assert [(c["_id"], c["parent_id"]) for c in before] == [
        (c["_id"], c["parent_id"]) for c in after
    ]
    assert all(c["status"] == "superseded" for c in after)
    _, body = load_document(path, corpus)
    assert all(body[c["start_char"] : c["end_char"]] == c["body"] for c in after)
