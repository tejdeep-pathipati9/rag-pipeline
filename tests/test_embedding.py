"""Check embedding input limits before a model can silently truncate source text."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src import embedding


@pytest.fixture
def model(monkeypatch, tokenizer):
    """Use a six-content-token limit, reserving two of eight positions for special tokens."""
    backend = SimpleNamespace(
        max_seq_length=8,
        tokenizer=SimpleNamespace(num_special_tokens_to_add=lambda pair: 2),
        get_embedding_dimension=lambda: 3,
        encode=Mock(return_value=SimpleNamespace(tolist=lambda: [[1.0, 0.0, 0.0]])),
    )
    monkeypatch.setattr(embedding, "SentenceTransformer", lambda *args, **kwargs: backend)
    monkeypatch.setattr(embedding, "ModelTokenizer", lambda *args, **kwargs: tokenizer)
    return embedding.EmbeddingModel("test-model", revision="test-revision"), backend


def test_embedding_accepts_full_content_budget(model):
    """The input budget accounts for the model's special-token overhead."""
    embedder, backend = model
    assert embedder.max_content_tokens == 6
    assert embedder.embed_documents(["one two three four five six"]) == [[1.0, 0.0, 0.0]]
    assert backend.encode.call_args.args[0] == ["one two three four five six"]


def test_oversized_text_is_rejected_before_model_encoding(model):
    """Missing source text must never be hidden by model truncation."""
    embedder, backend = model
    with pytest.raises(ValueError, match="token limit"):
        embedder.embed_documents(["one two three four five six seven"])
    backend.encode.assert_not_called()


def test_empty_embedding_batch_skips_model_encoding(model):
    """No input should produce no embeddings or model work."""
    embedder, backend = model
    assert embedder.embed_documents([]) == []
    backend.encode.assert_not_called()
