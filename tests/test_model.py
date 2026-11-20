"""Check grounded generation, structured decisions and citation references offline."""

import json
from types import SimpleNamespace
from unittest.mock import Mock

import httpx2
import pytest
from anthropic import AnthropicFoundry
from pydantic import ValidationError

from src.model import FlightAnswer, generate_answer


@pytest.fixture
def evidence():
    """One retrieved chunk, including ranking data that does not belong in the prompt."""
    return [
        {
            "_id": "chunk-care",
            "body": "Original Hotel Policy Text.",
            "document_id": "NS-CARE-2026",
            "document_type": "policy",
            "title": "Passenger Care",
            "version": "2.0",
            "effective_from": "2026-01-01",
            "status": "current",
            "section_ids": ["4", "4.1"],
            "source_path": "corpus/policies/02_passenger_care_2026.md",
            "rrf_score": 0.03,
            "rerank_score": 4.0,
            "vector_score": 0.8,
            "body_vector": [0.1, 0.2],
        }
    ]


@pytest.fixture
def response_data():
    """Structurally valid review decisions; this fixture is not a policy-answer oracle."""
    return {
        "summary": "More passenger facts are needed.",
        **{
            option: {
                "status": "NEEDS_REVIEW",
                "explanation": "The travel facts are incomplete.",
                "citations": ["NS-CARE-2026#4.1"],
                "missing_facts": ["Travel date and itinerary"],
            }
            for option in ("rebooking", "hotel", "refund")
        },
    }


def make_client(answer):
    """Stand in for the Azure SDK's structured-output response."""
    client = Mock(spec=AnthropicFoundry)
    client.messages.parse.return_value = SimpleNamespace(parsed_output=answer)
    return client


def test_generation_sends_retrieved_evidence_and_returns_three_decisions(evidence, response_data):
    """Use the configured deployment and preserve source text/metadata in the model context."""
    answer = FlightAnswer.model_validate(response_data)
    client = make_client(answer)

    result = generate_answer("Can I receive a hotel?", evidence, client, model="my-opus-deployment")

    assert result == answer
    request = client.messages.parse.call_args.kwargs
    assert request["model"] == "my-opus-deployment"
    assert request["output_format"] is FlightAnswer
    payload = json.loads(request["messages"][0]["content"])
    assert payload["question"] == "Can I receive a hotel?"
    assert payload["evidence"][0]["body"] == evidence[0]["body"]
    assert payload["evidence"][0]["version"] == "2.0"
    assert payload["evidence"][0]["section_ids"] == ["4", "4.1"]
    assert "rrf_score" not in payload["evidence"][0]
    assert "rerank_score" not in payload["evidence"][0]
    assert "body_vector" not in payload["evidence"][0]


def test_unknown_citations_are_rejected(evidence, response_data):
    """A model cannot cite a document or section absent from the supplied chunks."""
    response_data["hotel"]["citations"] = ["MADE-UP-POLICY#9"]
    client = make_client(FlightAnswer.model_validate(response_data))
    with pytest.raises(ValueError, match="unretrieved citation"):
        generate_answer("Hotel rules?", evidence, client, model="test")


def test_definite_decision_requires_a_citation(evidence, response_data):
    """Do not accept an uncited eligibility assertion."""
    response_data["hotel"].update(status="ELIGIBLE", citations=[], missing_facts=[])
    client = make_client(FlightAnswer.model_validate(response_data))
    with pytest.raises(ValueError, match="requires a citation"):
        generate_answer("Hotel rules?", evidence, client, model="test")


def test_review_decision_explains_missing_facts(evidence, response_data):
    """A review status must state what prevents a decision."""
    response_data["hotel"]["missing_facts"] = []
    client = make_client(FlightAnswer.model_validate(response_data))
    with pytest.raises(ValueError, match="missing facts"):
        generate_answer("Hotel rules?", evidence, client, model="test")


@pytest.mark.parametrize(
    ("option", "citations", "missing", "error"),
    [
        ("refund", ["NS-CARE-2026#4.1"], ["Passenger choice"], None),
        ("refund", [], ["Passenger choice"], "requires a citation"),
        ("refund", ["NS-CARE-2026#4.1"], [], "missing facts"),
        ("hotel", ["NS-CARE-2026#4.1"], ["Passenger choice"], "only to refunds"),
    ],
)
def test_pending_passenger_decision_is_a_cited_refund_status(
    evidence, response_data, option, citations, missing, error
):
    response_data[option].update(
        status="NEEDS_PASSENGER_DECISION", citations=citations, missing_facts=missing
    )
    client = make_client(FlightAnswer.model_validate(response_data))
    if error:
        with pytest.raises(ValueError, match=error):
            generate_answer("What are my options?", evidence, client, model="test")
    else:
        answer = generate_answer("What are my options?", evidence, client, model="test")
        assert answer.refund.status == "NEEDS_PASSENGER_DECISION"


def test_no_evidence_returns_review_without_calling_model():
    """Missing retrieval results produce abstention instead of an unsupported model answer."""
    client = make_client(None)
    answer = generate_answer("Hotel rules?", [], client, model="test")
    for option in (answer.rebooking, answer.hotel, answer.refund):
        assert option.status == "NEEDS_REVIEW"
        assert option.citations == []
        assert option.missing_facts
    client.messages.parse.assert_not_called()


def test_missing_structured_output_fails_clearly(evidence):
    """Refusals or incomplete responses must not become accepted eligibility decisions."""
    client = make_client(None)
    with pytest.raises(RuntimeError, match="structured answer"):
        generate_answer("Hotel rules?", evidence, client, model="test")


def test_empty_question_fails_before_calling_model(evidence):
    client = make_client(None)
    with pytest.raises(ValueError, match="Question"):
        generate_answer(" ", evidence, client, model="test")
    client.messages.parse.assert_not_called()


def test_response_schema_rejects_unknown_statuses(response_data):
    response_data["hotel"]["status"] = "PROBABLY"
    with pytest.raises(ValidationError):
        FlightAnswer.model_validate(response_data)


def test_foundry_sdk_serializes_schema_and_parses_answer_without_network(evidence, response_data):
    """Exercise the real SDK request/response path against an in-memory HTTP transport."""

    def respond(request):
        assert request.url.path == "/anthropic/v1/messages"
        payload = json.loads(request.content)
        assert payload["model"] == "my-opus-deployment"
        assert payload["output_config"]["format"]["type"] == "json_schema"
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "my-opus-deployment",
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
        answer = generate_answer("Hotel rules?", evidence, client, model="my-opus-deployment")

    assert answer.model_dump() == response_data
