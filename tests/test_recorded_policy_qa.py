"""Replay actual Pinecone/Azure results against the current corpus; no network calls."""

import hashlib
import json
from pathlib import Path

import pytest

from scripts.evaluate import GOLD_SET, load_cases, score_case
from src.documents import _section_ranges, load_document
from src.model import SYSTEM_PROMPT, PolicyAnswer

RECORDING = json.loads(Path("evaluation/policy_qa_recorded.json").read_text())
CASES = {case["case_id"]: case for case in load_cases()}


@pytest.mark.parametrize("record", RECORDING["cases"], ids=lambda record: record["case_id"])
def test_recorded_policy_retrieval_and_answer(record):
    assert hashlib.sha256(GOLD_SET.read_bytes()).hexdigest() == RECORDING["dataset_sha256"]
    assert hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest() == RECORDING["prompt_sha256"]
    assert (
        hashlib.sha256(Path("specifications/corpus_manifest.yaml").read_bytes()).hexdigest()
        == RECORDING["corpus_manifest_sha256"]
    )
    case = CASES[record["case_id"]]
    assert record["question"] == case["question"]
    for hit in record["matches"]:
        metadata, body = load_document(Path(hit["source_path"]), Path("corpus"))
        assert metadata["document_id"] == hit["document_id"]
        assert metadata["source_checksum"] == hit["source_checksum"]
        start, end = int(hit["start_char"]), int(hit["end_char"])
        assert 0 <= start < end <= len(body)
        assert hit["section_ids"] == [
            section for section, a, b in _section_ranges(body) if a < end and start < b
        ]
    answer = PolicyAnswer.model_validate(record["answer"])
    scores = score_case(case, record["matches"], answer.model_dump())
    assert scores == record["scores"]
    # A complete equivalent path can support an answer without the canonical section.
    context = {f"{h['document_id']}#{s}" for h in record["matches"] for s in h["section_ids"]}
    paths = case.get("citation_paths", [[ref] for ref in case["expected_sections"]])
    assert any(set(path) <= context for path in paths)
    assert scores["answer_pass"]
