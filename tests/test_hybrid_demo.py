"""Check the observed keyword-search win against the actual source text."""

import json
from pathlib import Path
from unittest.mock import Mock

from scripts import hybrid_demo as demo
from src.documents import load_document


def test_recorded_hybrid_finds_code_clause_missing_from_dense_top_five():
    record = json.loads(demo.RECORDING.read_text())
    target = record["expected_section"]
    found = {}
    for method in ("dense", "hybrid"):
        found[method] = []
        for hit in record[method]:
            metadata, body = load_document(Path(hit["source_path"]), Path("corpus"))
            assert metadata["source_checksum"] == hit["source_checksum"]
            assert body[int(hit["start_char"]):int(hit["end_char"])] == hit["body"]
            refs = [f"{hit['document_id']}#{s}" for s in hit["section_ids"]]
            if target in refs:
                found[method].append(hit)
    assert not found["dense"]
    assert len(found["hybrid"]) == 1
    hit = found["hybrid"][0]
    assert hit["keyword_rank"] == 1 and "vector_rank" not in hit
    assert "NO_CURRENT_INVENTORY" in hit["body"]


def test_default_demo_is_explicitly_recorded_and_does_not_connect(monkeypatch, capsys):
    client = Mock()
    monkeypatch.setattr(demo, "Pinecone", client)
    demo.main([])
    client.assert_not_called()
    assert "RECORDED LIVE SEARCH RESULTS" in capsys.readouterr().out
