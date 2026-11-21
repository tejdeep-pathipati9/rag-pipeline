"""Verify the actual before/after recording offline, including its source lineage."""

import hashlib
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts import source_failure_demo as demo
from src.documents import _section_ranges, load_document
from src.model import SYSTEM_PROMPT, PolicyAnswer

RECORD = json.loads(demo.RECORDING.read_text())
CARE_PATH = Path("corpus/policies/02_passenger_care_2026.md")


@pytest.mark.parametrize("name", RECORD["stages"])
def test_recorded_answers_cite_exact_source_spans(name, tmp_path):
    captured_corpus = tmp_path / "corpus"
    for source_path, text in RECORD["corrected_sources"].items():
        path = tmp_path / source_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    if name == "broken_live":
        (tmp_path / CARE_PATH).write_text(RECORD["broken_care_source"])
    stage = RECORD["stages"][name]
    for hit in stage["evidence"]:
        metadata, body = load_document(tmp_path / hit["source_path"], captured_corpus)
        assert metadata["source_checksum"] == hit["source_checksum"]
        start, end = int(hit["start_char"]), int(hit["end_char"])
        assert 0 <= start < end <= len(body)
        assert body[start:end] == hit["body"]
        assert hit["section_ids"] == [
            section for section, a, b in _section_ranges(body) if a < end and start < b
        ]
    answer = PolicyAnswer.model_validate(stage["answer"])
    allowed = {
        f"{hit['document_id']}#{section}"
        for hit in stage["evidence"] for section in hit["section_ids"]
    }
    assert set(answer.citations) <= allowed
    assert "NS-CARE-2026#4.5" in answer.citations


def test_source_only_repair_preserves_prompt_and_evidence_slots():
    manifest = RECORD["manifest"]
    assert hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest() == manifest["prompt_sha256"]
    assert (
        hashlib.sha256(RECORD["corrected_sources"][str(CARE_PATH)].encode()).hexdigest()
        == manifest["corrected_sha256"]
    )
    assert manifest["corrected_sha256"] == manifest["production_source_sha256"]
    assert (
        hashlib.sha256(RECORD["broken_care_source"].encode()).hexdigest()
        == manifest["broken_sha256"]
    )
    broken = RECORD["stages"]["broken_live"]
    repaired = RECORD["stages"]["source_only_repaired_replay"]
    for before, after in zip(broken["evidence"], repaired["evidence"], strict=True):
        for field in (
            "document_id", "section_ids", "title", "version", "effective_from",
            "effective_to", "status", "source_path",
        ):
            assert before.get(field) == after.get(field)
    changed = [
        before["document_id"]
        for before, after in zip(broken["evidence"], repaired["evidence"], strict=True)
        if before["body"] != after["body"]
    ]
    assert changed == ["NS-CARE-2026"]
    # Check the observed outcomes, not a general-purpose semantic accuracy claim.
    assert "not a standard benefit" in broken["answer"]["answer"]
    assert "it is a standard benefit, not a discretionary courtesy" in repaired["answer"]["answer"]
    assert "standard benefit, not a discretionary courtesy" in (
        RECORD["stages"]["corrected_live"]["answer"]["answer"]
    )


def test_demo_default_shows_recorded_results_without_api_calls(monkeypatch, capsys):
    client, generate, config = Mock(), Mock(), Mock()
    monkeypatch.setattr(demo, "AnthropicFoundry", client)
    monkeypatch.setattr(demo, "generate_answer", generate)
    monkeypatch.setattr(demo.AppConfig, "from_env", config)
    demo.main([])
    output = capsys.readouterr().out
    assert "RECORDED LIVE API RESULTS" in output
    assert "not a standard benefit" in output and "it is a standard benefit" in output
    client.assert_not_called()
    generate.assert_not_called()
    config.assert_not_called()


def test_export_matches_the_exact_sources_used_in_the_failure_and_repair(tmp_path, capsys):
    demo.main(["--export-dir", str(tmp_path)])
    for source_path, text in RECORD["corrected_sources"].items():
        assert (tmp_path / "corrected" / source_path).read_text() == text
        broken = (tmp_path / "broken" / source_path).read_text()
        expected = RECORD["broken_care_source"] if source_path == str(CARE_PATH) else text
        assert broken == expected
        assert 500 <= len(broken.split("---", 2)[2].split()) <= 800
    assert "Exported exact demonstration sources" in capsys.readouterr().out
