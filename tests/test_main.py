"""Check actionable command errors without model downloads or Pinecone requests."""

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
