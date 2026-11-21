"""Check actionable command errors without model downloads or Pinecone requests."""

import json
from functools import partial
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import pytest
from pinecone import NotFoundError

from src import __main__ as cli
from src import config as config_module
from src import terminal
from src.config import ChunkingConfig
from src.model import PolicyAnswer


def test_default_prompt_reuses_models_and_clients_without_ingestion(monkeypatch, capsys):
    embeddings = SimpleNamespace(
        model_name="test", revision="test", dimension=384, tokenizer=Mock()
    )
    load_embeddings = Mock(return_value=embeddings)
    load_reranker = Mock()
    pinecone = MagicMock()
    pinecone.__enter__.return_value = pinecone
    pinecone.describe_index.return_value.to_dict.return_value = {"host": "https://test-index"}
    foundry = MagicMock()
    evidence = [{"document_id": "CARE", "title": "Passenger Care Policy"}]
    retrieve = Mock(return_value=[])
    generate = Mock(return_value=PolicyAnswer(
        answer="Hotel coverage depends on the cause.", citations=["CARE#4.1"],
        missing_information=["The confirmed cause"],
    ))
    prepare, ingest = Mock(), Mock()
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", load_embeddings)
    monkeypatch.setattr(cli, "CrossEncoder", load_reranker)
    monkeypatch.setattr(cli, "Pinecone", Mock(return_value=pinecone))
    monkeypatch.setattr(cli, "AnthropicFoundry", foundry)
    monkeypatch.setattr(cli, "validate_index", Mock())
    monkeypatch.setattr(terminal, "retrieve_hybrid", retrieve)
    monkeypatch.setattr(terminal, "rerank_results", Mock(return_value=[]))
    monkeypatch.setattr(terminal, "assemble_evidence", Mock(return_value=evidence))
    monkeypatch.setattr(terminal, "generate_answer", generate)
    monkeypatch.setattr(cli, "prepare_chunks", prepare)
    monkeypatch.setattr(cli, "ingest_chunks", ingest)
    for key in (
        "PINECONE_API_KEY", "PINECONE_INDEX_NAME", "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"
    ):
        monkeypatch.setenv(key, "test")
    inputs = iter(["", "/help", "Hotel?", "Refund?", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cli.main([])

    load_embeddings.assert_called_once()
    load_reranker.assert_called_once()
    foundry.assert_called_once()
    prepare.assert_not_called()
    ingest.assert_not_called()
    assert [call.args[0] for call in retrieve.call_args_list] == ["Hotel?", "Refund?"]
    assert all(call.kwargs == {"namespace": "policy-qa-parent-child-200-40-v1", "top_k": 20}
               for call in retrieve.call_args_list)
    assert generate.call_count == 2
    assert all(call.args[1] == evidence for call in generate.call_args_list)
    assert all(call.args[2] is foundry.return_value.__enter__.return_value
               for call in generate.call_args_list)
    foundry.return_value.__exit__.assert_called_once()
    pinecone.__exit__.assert_called_once()
    output = capsys.readouterr().out
    assert "Try:" in output
    assert output.count("Passenger Care Policy (CARE), §4.1") == 2
    assert "The confirmed cause" in output
    assert "Goodbye." in output


@pytest.mark.parametrize("stop", [EOFError, KeyboardInterrupt])
def test_prompt_recovers_from_failed_question_and_exits_cleanly(monkeypatch, capsys, stop):
    monkeypatch.setattr("builtins.input", Mock(side_effect=["Hotel?", "Refund?", stop()]))
    retrieve = Mock(side_effect=[RuntimeError("internal service detail"), []])
    monkeypatch.setattr(terminal, "retrieve_hybrid", retrieve)
    monkeypatch.setattr(terminal, "rerank_results", Mock(return_value=[]))
    monkeypatch.setattr(terminal, "assemble_evidence", Mock(return_value=[]))
    generate = Mock(return_value=PolicyAnswer(answer="Please confirm the delay.", citations=[],
                                                missing_information=[]))
    monkeypatch.setattr(terminal, "generate_answer", generate)

    terminal.interactive_session(Mock(), Mock(), Mock(), Mock(), namespace="test", model="test")

    assert retrieve.call_count == 2
    generate.assert_called_once()
    output = capsys.readouterr().out
    assert "Please try again" in output
    assert "Please confirm the delay." in output
    assert "internal service detail" not in output
    assert "Goodbye." in output


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
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=[]))
    monkeypatch.setattr(cli, "Pinecone", Mock(return_value=client))
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "missing-index")

    with pytest.raises(SystemExit) as error:
        cli.main(["--namespace", "test", "--ingest"])

    assert error.value.code == 2
    message = capsys.readouterr().err
    assert "missing-index" in message
    assert "API key's project" in message
    assert "Traceback" not in message
    client.Index.assert_not_called()


@pytest.mark.parametrize(
    ("default_strategy", "override", "expected"),
    [("recursive", None, "recursive"), ("markdown", None, "markdown"),
     ("markdown", "parent-child", "parent-child")],
)
def test_ingestion_dry_run_still_prepares_without_contacting_pinecone(
    monkeypatch, tokenizer, capsys, default_strategy, override, expected
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
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=model))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=[]))
    monkeypatch.setattr(cli, "Pinecone", pinecone)
    monkeypatch.setattr(cli, "CrossEncoder", reranker)
    monkeypatch.setattr(cli, "ChunkingConfig", partial(
        ChunkingConfig, strategy=default_strategy, chunk_size=100, overlap=20
    ))

    arguments = ["--namespace", "test", "--dry-run"]
    if override:
        arguments.extend(["--chunk-strategy", override, "--chunk-size", "80", "--overlap", "10"])
    cli.main(arguments)

    pinecone.assert_not_called()
    reranker.assert_not_called()
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True
    assert output["upserted"] == 0
    assert output["chunk_strategy"] == expected
    assert output["chunk_size"] == (80 if override else 100)
    assert output["overlap"] == (10 if override else 20)


def test_ingestion_uploads_to_selected_namespace_without_loading_answer_models(
    monkeypatch, tokenizer, capsys
):
    embeddings = SimpleNamespace(
        model_name="test", revision="test", dimension=384,
        max_content_tokens=254, tokenizer=tokenizer,
    )
    chunks = [{"document_id": "CARE", "body": "Hotel rules."}]
    pinecone = MagicMock()
    pinecone.__enter__.return_value = pinecone
    pinecone.describe_index.return_value.to_dict.return_value = {"host": "https://test-index"}
    ingest, reranker, foundry = Mock(return_value=1), Mock(), Mock()
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", Mock(return_value=embeddings))
    monkeypatch.setattr(cli, "prepare_chunks", Mock(return_value=chunks))
    monkeypatch.setattr(cli, "validate_index", Mock())
    monkeypatch.setattr(cli, "Pinecone", Mock(return_value=pinecone))
    monkeypatch.setattr(cli, "ingest_chunks", ingest)
    monkeypatch.setattr(cli, "CrossEncoder", reranker)
    monkeypatch.setattr(cli, "AnthropicFoundry", foundry)
    monkeypatch.setenv("PINECONE_API_KEY", "test")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "test-index")
    for field in ("LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"):
        monkeypatch.delenv(field, raising=False)

    cli.main(["--ingest", "--namespace", "custom", "--batch-size", "8"])

    ingest.assert_called_once_with(
        chunks, embeddings, pinecone.Index.return_value.__enter__.return_value,
        namespace="custom", batch_size=8,
    )
    reranker.assert_not_called()
    foundry.assert_not_called()
    output = json.loads(capsys.readouterr().out)
    assert output["upserted"] == 1
    assert output["documents"] == 1
    assert output["namespace"] == "custom"


def test_missing_generation_configuration_fails_before_loading_model(monkeypatch, capsys):
    load_model = Mock()
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(cli, "EmbeddingModel", load_model)
    for field in ("LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"):
        monkeypatch.delenv(field, raising=False)
    with pytest.raises(SystemExit):
        cli.main([])
    assert "LLM_BASE_URL" in capsys.readouterr().err
    load_model.assert_not_called()


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["--chunk-strategy", "markdown"], "applies to ingestion"),
        (["--ingest", "--dry-run"], "not allowed with argument"),
        (["--question", "Hotel?"], "unrecognized arguments"),
    ],
)
def test_cli_rejects_invalid_arguments_before_loading_models(
    monkeypatch, capsys, arguments, message
):
    load_model = Mock()
    monkeypatch.setattr(cli, "EmbeddingModel", load_model)

    with pytest.raises(SystemExit) as error:
        cli.main(["--namespace", "test", *arguments])

    assert error.value.code == 2
    assert message in capsys.readouterr().err
    load_model.assert_not_called()
