"""Check actionable command errors without model downloads or Pinecone requests."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import pytest
from pinecone import NotFoundError

from src import __main__ as cli


def test_missing_index_reports_configuration_error(monkeypatch, tokenizer, capsys):
    """A missing index should explain what to fix instead of displaying an SDK traceback."""
    model = SimpleNamespace(
        model_name="test-model",
        revision="test",
        dimension=3,
        max_content_tokens=254,
        tokenizer=tokenizer,
    )
    client = MagicMock()
    client.__enter__.return_value = client
    client.describe_index.side_effect = NotFoundError("Resource missing-index not found")
    monkeypatch.setattr(cli, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=[]))
    monkeypatch.setattr(cli, "Pinecone", Mock(return_value=client))
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "missing-index")

    with pytest.raises(SystemExit) as error:
        cli.main(["--namespace", "test"])

    assert error.value.code == 2
    message = capsys.readouterr().err
    assert "missing-index" in message
    assert "API key's project" in message
    assert "Traceback" not in message
    client.Index.assert_not_called()


@pytest.mark.parametrize("mode", ["retrieval", "answer", "details", "json"])
@pytest.mark.parametrize("empty_results", [False, True])
def test_question_command_runs_retrieval_without_preparing_or_upserting(
    monkeypatch, tokenizer, capsys, mode, empty_results
):
    """Retrieval queries existing records and never starts corpus ingestion."""
    model = SimpleNamespace(
        model_name="test-model",
        revision="test",
        dimension=3,
        max_content_tokens=254,
        tokenizer=tokenizer,
    )
    client = MagicMock()
    client.__enter__.return_value = client
    client.describe_index.return_value.to_dict.return_value = {"host": "https://test-index"}
    index = client.Index.return_value.__enter__.return_value
    hits = [
        {
            "_id": "chunk-1",
            "rrf_score": 1 / 61,
            "body": "Hotel rules.",
            "section_ids": ["4.1", "4.2"],
            "title": "Passenger Care Policy",
            "document_id": "CARE",
        },
        {"_id": "chunk-2", "rrf_score": 1 / 62, "body": "Overnight rules.", "section_ids": ["4.2"]},
    ]
    if empty_results:
        hits = []
    reranker = Mock()
    reranker.predict.return_value = [0.1, 0.9]
    load_reranker = Mock(return_value=reranker)
    monkeypatch.setattr(cli, "CrossEncoder", load_reranker)
    hide_progress = Mock()
    monkeypatch.setattr(cli.transformers_logging, "disable_progress_bar", hide_progress)
    reranked_hits = (
        []
        if empty_results
        else [{**hits[1], "rerank_score": 0.9}, {**hits[0], "rerank_score": 0.1}]
    )
    monkeypatch.setattr(cli, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    prepare = Mock()
    upsert = Mock()
    retrieve = Mock(return_value=hits)
    monkeypatch.setattr(cli, "prepare_chunks", prepare)
    monkeypatch.setattr(cli, "ingest_chunks", upsert)
    monkeypatch.setattr(cli, "retrieve_hybrid", retrieve)
    monkeypatch.setattr(cli, "validate_index", Mock())
    monkeypatch.setattr(cli, "Pinecone", Mock(return_value=client))
    foundry = MagicMock()
    review = {
        "status": "NEEDS_REVIEW",
        "explanation": "The overnight wait is unconfirmed.",
        "citations": [] if empty_results else ["CARE#4.1", "CARE#4.2"],
        "missing_facts": ["The next flight's departure time"],
    }
    answer = cli.FlightAnswer.model_validate(
        {
            "summary": "Please confirm the overnight wait.",
            **dict.fromkeys(("rebooking", "hotel", "refund"), review),
        }
    )
    generation = Mock(return_value=answer)
    monkeypatch.setattr(cli, "AnthropicFoundry", foundry)
    monkeypatch.setattr(cli, "generate_answer", generation)
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "test-index")
    monkeypatch.setenv("LLM_API_KEY", "test-llm-key")
    monkeypatch.setenv("LLM_MODEL", "my-opus-deployment")
    monkeypatch.setenv("LLM_BASE_URL", "https://example.services.ai.azure.com/anthropic")

    arguments = ["--namespace", "recursive-test", "--question", "Hotel rules?"]
    if mode != "retrieval":
        arguments.append("--generate")
    if mode == "json":
        arguments.append("--json")
    if mode == "details":
        arguments.append("--details")
    cli.main(arguments)

    retrieve.assert_called_once_with("Hotel rules?", model, index, namespace="recursive-test")
    prepare.assert_not_called()
    upsert.assert_not_called()
    stdout = capsys.readouterr().out
    if mode in {"answer", "details"}:
        assert stdout.startswith("Please confirm the overnight wait.\n")
        assert "Hotel · Needs review" in stdout
        if mode == "answer":
            hide_progress.assert_called_once()
            assert "The overnight wait is unconfirmed." not in stdout
            assert "The next flight's departure time" not in stdout
            assert ("CARE §4.1, §4.2" in stdout) == bool(hits)
        else:
            hide_progress.assert_not_called()
            assert "The next flight's departure time" in stdout
            assert ("Passenger Care Policy (CARE), §4.1, §4.2" in stdout) == bool(hits)
        assert '"matches"' not in stdout
        assert '"rrf_score"' not in stdout
    else:
        output = json.loads(stdout)
        assert output["top_k_per_method"] == 10
        assert output["retrieval_method"] == "hybrid"
        assert output["matches"] == reranked_hits
        assert output["reranker_model"] == cli.RERANKER_MODEL
        assert output["reranker_revision"] == cli.RERANKER_REVISION
        if mode == "json":
            assert output["answer"] == answer.model_dump()
    if empty_results:
        load_reranker.assert_not_called()
        reranker.predict.assert_not_called()
    else:
        load_reranker.assert_called_once()
    if mode != "retrieval":
        llm = foundry.return_value.__enter__.return_value
        generation.assert_called_once_with(
            "Hotel rules?", reranked_hits, llm, model="my-opus-deployment"
        )
    else:
        generation.assert_not_called()
        foundry.assert_not_called()


def test_ingestion_dry_run_still_prepares_without_contacting_pinecone(
    monkeypatch, tokenizer, capsys
):
    """Adding retrieval must preserve the existing write-free ingestion preview."""
    model = SimpleNamespace(
        model_name="test-model",
        revision="test",
        dimension=3,
        max_content_tokens=254,
        tokenizer=tokenizer,
    )
    pinecone = Mock()
    reranker = Mock()
    monkeypatch.setattr(cli, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=[]))
    monkeypatch.setattr(cli, "Pinecone", pinecone)
    monkeypatch.setattr(cli, "CrossEncoder", reranker)

    cli.main(["--namespace", "test", "--dry-run"])

    pinecone.assert_not_called()
    reranker.assert_not_called()
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True
    assert output["upserted"] == 0


def test_generation_requires_question_before_loading_model(monkeypatch):
    load_model = Mock()
    monkeypatch.setattr(cli, "EmbeddingModel", load_model)
    with pytest.raises(SystemExit):
        cli.main(["--namespace", "test", "--generate"])
    load_model.assert_not_called()


def test_missing_generation_configuration_fails_before_loading_model(monkeypatch, capsys):
    load_model = Mock()
    monkeypatch.setattr(cli, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", load_model)
    for field in ("LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"):
        monkeypatch.delenv(field, raising=False)
    with pytest.raises(SystemExit):
        cli.main(["--namespace", "test", "--question", "Hotel rules?", "--generate"])
    assert "LLM_BASE_URL" in capsys.readouterr().err
    load_model.assert_not_called()
