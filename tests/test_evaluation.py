"""Check evaluation scoring and split selection without external services."""

import pytest

from src.evaluation import score_case, select_cases


def test_selection_defaults_to_only_the_requested_split():
    development = select_cases("development", [])
    assert len(development) == 8
    assert {case["split"] for case in development} == {"development"}
    with pytest.raises(ValueError, match="Cases outside the development split"):
        select_cases("development", ["FR-R028"])


def test_scoring_checks_complete_evidence_paths_and_separates_the_status():
    case = {
        "expected": {
            "refund": {
                "status": "NEEDS_PASSENGER_DECISION",
                "compatible_status": "NEEDS_REVIEW",
                "required": {
                    "arrival": [["P#1", "O#2"], ["O#3"]],
                    "choice": [["O#4"]],
                },
            },
        }
    }
    hits = [{"document_id": "P", "section_ids": ["1"]}]
    hits.extend({"document_id": "OTHER", "section_ids": ["1"]} for _ in range(4))
    hits.append({"document_id": "O", "section_ids": ["3"]})
    result = score_case(case, hits, {"refund": {"status": "NEEDS_REVIEW"}})

    assert result["hit_at_5"] is True
    refund = result["decisions"]["refund"]
    assert refund["claims_at_5"] == 0
    assert refund["missing_context_claims"] == ["choice"]
    assert refund["exact"] is False
    assert refund["requires_compatibility_review"] is True
