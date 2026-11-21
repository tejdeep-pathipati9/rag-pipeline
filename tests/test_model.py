"""Validate direct policy answers and the real SDK schema path without network calls."""

import json
from types import SimpleNamespace
from unittest.mock import Mock

import httpx2
import pytest
from anthropic import AnthropicFoundry
from pydantic import ValidationError

from src.model import PolicyAnswer, generate_answer


@pytest.fixture
def evidence():
    return [
        {
            "_id": "care",
            "body": "Original policy text.",
            "document_id": "NS-CARE-2026",
            "document_type": "policy",
            "title": "Passenger Care",
            "version": "2.1",
            "effective_from": "2026-01-01",
            "status": "current",
            "section_ids": ["4.1"],
            "source_path": "corpus/policies/02_passenger_care_2026.md",
            "rerank_score": 4.0,
            "body_vector": [0.1, 0.2],
        }
    ]


@pytest.fixture
def response_data():
    return {
        "answer": "Hotel coverage requires an overnight stay away from home.",
        "citations": ["NS-CARE-2026#4.1"],
        "missing_information": [],
    }


def make_client(answer):
    client = Mock(spec=AnthropicFoundry)
    client.messages.parse.return_value = SimpleNamespace(parsed_output=answer)
    return client


def test_generation_preserves_policy_evidence_and_excludes_scores(evidence, response_data):
    answer = PolicyAnswer.model_validate(response_data)
    client = make_client(answer)
    assert (
        generate_answer(
            "What is the hotel policy?", evidence, client, model="deployment", as_of="2026-11-20"
        )
        == answer
    )
    request = client.messages.parse.call_args.kwargs
    assert request["model"] == "deployment"
    assert request["output_format"] is PolicyAnswer
    payload = json.loads(request["messages"][0]["content"])
    assert payload["question"] == "What is the hotel policy?"
    assert payload["as_of_date"] == "2026-11-20"
    assert payload["evidence"][0]["body"] == evidence[0]["body"]
    assert payload["evidence"][0]["version"] == "2.1"
    assert payload["allowed_citations"] == ["NS-CARE-2026#4.1"]
    assert "rerank_score" not in payload["evidence"][0]
    assert "body_vector" not in payload["evidence"][0]


def test_current_questions_receive_a_reference_date_without_rewriting_user_text(
    evidence, response_data
):
    client = make_client(PolicyAnswer(**response_data))
    question = "Do crew delays qualify for a hotel?"
    generate_answer(question, evidence, client, model="deployment")
    payload = json.loads(client.messages.parse.call_args.kwargs["messages"][0]["content"])
    assert payload["question"] == question
    from datetime import date

    date.fromisoformat(payload["as_of_date"])


def test_unknown_citation_is_rejected(evidence, response_data):
    response_data["citations"] = ["INVENTED#9"]
    with pytest.raises(ValueError, match="unretrieved citation"):
        generate_answer(
            "Hotel policy?", evidence, make_client(PolicyAnswer(**response_data)), model="x"
        )


def test_uncited_answer_must_explain_missing_evidence(evidence, response_data):
    response_data["citations"] = []
    with pytest.raises(ValueError, match="missing evidence"):
        generate_answer(
            "Hotel policy?", evidence, make_client(PolicyAnswer(**response_data)), model="x"
        )
    response_data["missing_information"] = ["Applicable policy clause"]
    assert generate_answer(
        "Hotel policy?", evidence, make_client(PolicyAnswer(**response_data)), model="x"
    ).missing_information


def test_no_evidence_abstains_without_calling_model():
    client = make_client(None)
    answer = generate_answer("Hotel policy?", [], client, model="x")
    assert answer.citations == []
    assert answer.missing_information
    client.messages.parse.assert_not_called()


def test_missing_structured_output_fails(evidence):
    with pytest.raises(RuntimeError, match="structured answer"):
        generate_answer("Hotel policy?", evidence, make_client(None), model="x")


def test_empty_question_rejected_before_model_call(evidence):
    client = make_client(None)
    with pytest.raises(ValueError, match="Question"):
        generate_answer(" ", evidence, client, model="x")
    client.messages.parse.assert_not_called()


def test_policy_schema_rejects_passenger_decision_fields(response_data):
    with pytest.raises(ValidationError):
        PolicyAnswer(**response_data, hotel={"status": "ELIGIBLE"})


def test_foundry_sdk_serializes_and_parses_policy_answer(evidence, response_data):
    def respond(request):
        assert request.url.path == "/anthropic/v1/messages"
        payload = json.loads(request.content)
        assert payload["model"] == "deployment"
        assert payload["output_config"]["format"]["type"] == "json_schema"
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "deployment",
                "content": [{"type": "text", "text": json.dumps(response_data)}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 100, "output_tokens": 100},
            },
        )

    with AnthropicFoundry(
        api_key="test-key",
        base_url="https://example.services.ai.azure.com/anthropic",
        http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
    ) as client:
        assert (
            generate_answer("Hotel policy?", evidence, client, model="deployment").model_dump()
            == response_data
        )
