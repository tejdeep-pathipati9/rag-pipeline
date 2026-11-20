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


def test_question_command_runs_retrieval_without_preparing_or_upserting(
    monkeypatch, tokenizer, capsys
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
    hits = [{"_id": "chunk-1", "rrf_score": 1 / 61, "body": "Hotel rules.", "section_ids": ["4.1"]}]
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
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "test-index")

    cli.main(["--namespace", "recursive-test", "--question", "Hotel rules?"])

    retrieve.assert_called_once_with("Hotel rules?", model, index, namespace="recursive-test")
    prepare.assert_not_called()
    upsert.assert_not_called()
    output = json.loads(capsys.readouterr().out)
    assert output["top_k_per_method"] == 10
    assert output["retrieval_method"] == "hybrid"
    assert output["matches"] == hits


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
    monkeypatch.setattr(cli, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=[]))
    monkeypatch.setattr(cli, "Pinecone", pinecone)

    cli.main(["--namespace", "test", "--dry-run"])

    pinecone.assert_not_called()
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True
    assert output["upserted"] == 0
