"""Check complete Pinecone payloads and upload failures without network calls."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src.chunking import RecursiveChunker
from src.documents import prepare_chunks
from src.ingestion import ingest_chunks, validate_index


@pytest.fixture
def embeddings():
    """Supply deterministic vectors to inspect transport behavior, not model quality."""
    return SimpleNamespace(
        model_name="test-model",
        revision="test-revision",
        dimension=3,
        embed_documents=Mock(side_effect=lambda texts: [[1.0, 0.0, 0.0] for text in texts]),
    )


def test_upserts_store_vectors_text_and_metadata_idempotently(corpus, tokenizer, embeddings):
    """Repeated upserts retain the same IDs and send only original text to the embedder."""
    chunks = prepare_chunks(corpus, RecursiveChunker(tokenizer, 6, 1))
    stored = {}

    def upsert(*, namespace, documents):
        assert namespace == "recursive-test"
        stored.update({document["_id"]: document for document in documents})
        return SimpleNamespace(upserted_count=len(documents))

    index = SimpleNamespace(documents=SimpleNamespace(upsert=Mock(side_effect=upsert)))
    for _run in range(2):
        assert ingest_chunks(
            chunks, embeddings, index, namespace="recursive-test", batch_size=2
        ) == len(chunks)

    assert len(stored) == len(chunks)
    for chunk in chunks:
        record = stored[chunk["_id"]]
        assert record["body_vector"] == [1.0, 0.0, 0.0]
        assert record["body"] == chunk["body"]
        assert record["section_ids"] == chunk["section_ids"]
        assert record["embedding_model"] == "test-model"
    embedded_texts = [
        text for call in embeddings.embed_documents.call_args_list for text in call.args[0]
    ]
    assert embedded_texts == [chunk["body"] for chunk in chunks] * 2


@pytest.mark.parametrize("vectors", [[], [[1.0]], [[float("nan"), 0.0, 0.0]]])
def test_bad_embedding_results_do_not_get_upserted(corpus, tokenizer, embeddings, vectors):
    """Reject missing, wrongly sized or invalid vectors instead of losing or corrupting chunks."""
    chunks = prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))
    embeddings.embed_documents.return_value = vectors
    embeddings.embed_documents.side_effect = None
    index = SimpleNamespace(documents=SimpleNamespace(upsert=Mock()))
    with pytest.raises(ValueError, match="embedding"):
        ingest_chunks(chunks, embeddings, index, namespace="test")
    index.documents.upsert.assert_not_called()


def test_index_schema_must_match_embedding_dimension():
    """An incompatible vector field fails before any upserts."""
    description = {
        "schema": {
            "fields": {
                "body": {"type": "string", "store_text": True},
                "body_vector": {"type": "dense_vector", "dimension": 384},
            }
        }
    }
    validate_index(description, 384)
    with pytest.raises(ValueError, match="dimension"):
        validate_index(description, 2048)


def test_incomplete_upsert_acknowledgement_is_not_reported_as_success(
    corpus, tokenizer, embeddings
):
    """Every submitted chunk must be acknowledged; a short count is a failed run."""
    chunks = prepare_chunks(corpus, RecursiveChunker(tokenizer, 100, 0))
    index = SimpleNamespace(
        documents=SimpleNamespace(upsert=Mock(return_value=SimpleNamespace(upserted_count=0)))
    )
    with pytest.raises(RuntimeError, match="every chunk"):
        ingest_chunks(chunks, embeddings, index, namespace="test")


@pytest.mark.parametrize(("namespace", "batch_size"), [("", 64), ("  ", 64), ("test", 0)])
def test_invalid_write_settings_fail_before_embedding(embeddings, namespace, batch_size):
    """Do not embed or write anything when the destination or batch size is invalid."""
    index = SimpleNamespace(documents=SimpleNamespace(upsert=Mock()))
    with pytest.raises(ValueError):
        ingest_chunks([], embeddings, index, namespace=namespace, batch_size=batch_size)
    embeddings.embed_documents.assert_not_called()
    index.documents.upsert.assert_not_called()
