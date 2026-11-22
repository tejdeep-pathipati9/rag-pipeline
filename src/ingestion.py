"""Embed prepared chunks and store their text, vectors and metadata in Pinecone."""

import math


def ingest_chunks(chunks, embeddings, index, *, namespace: str, batch_size: int = 64) -> int:
    """Embed prepared chunks, upsert them, and return the acknowledged record count.

    Each input record must contain ``_id``, ``body`` and source metadata from
    prepare_chunks(). Only the body is embedded; copies of the records receive
    the vectors and embedding-model identity before upload. Inputs are unchanged.

    Use a namespace for one corpus/model/chunking configuration. Repeated IDs
    overwrite existing records; this function does not delete obsolete chunks.
    Writes happen per batch, so earlier batches remain if a later batch fails.

    Raises ValueError for invalid settings or embedding output, and RuntimeError
    if Pinecone does not acknowledge a full batch. Service errors propagate.
    """
    if not namespace.strip():
        raise ValueError("An explicit Pinecone namespace is required.")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive.")

    total = 0
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]

        # Position links a vector to its source: vectors[i] must describe batch[i].
        texts = [chunk["body"] for chunk in batch]
        vectors = embeddings.embed_documents(texts)
        if len(vectors) != len(batch):
            raise ValueError("The embedding result count does not match the chunk count.")

        # Keep the searchable body and citation metadata beside the dense vector.
        documents = []
        for chunk, vector in zip(batch, vectors, strict=True):
            # Reject unusable vectors before submitting this batch to Pinecone.
            if len(vector) != embeddings.dimension or not all(
                math.isfinite(value) for value in vector
            ):
                raise ValueError("Invalid embedding dimension or non-finite embedding values.")

            document = chunk.copy()
            document["body_vector"] = vector
            document["embedding_model"] = embeddings.model_name
            document["embedding_revision"] = embeddings.revision
            documents.append(document)

        # Stable IDs make an unchanged rerun overwrite the same records.
        # Acknowledgement confirms the write; fetch/search visibility can lag behind it.
        response = index.documents.upsert(namespace=namespace, documents=documents)
        if response.upserted_count != len(documents):
            raise RuntimeError("Pinecone did not acknowledge every chunk in the batch.")
        total += response.upserted_count

    return total


def validate_index(description: dict, embedding_dimension: int) -> None:
    """Check that Pinecone can store the text and the model's vector dimension.

    Inspect a describe_index() dictionary without changing the remote index.
    The schema needs a dense ``body_vector`` field with the model's dimension
    and a string ``body`` field whose text can be returned during retrieval.
    Other uploaded fields, such as document_id and section_ids, are metadata.
    Raise ValueError when these requirements are not met.
    """
    fields = description.get("schema", {}).get("fields", {})
    vector_field = fields.get("body_vector", {})
    if vector_field.get("type") != "dense_vector":
        raise ValueError("Pinecone needs a body_vector dense_vector field.")
    if vector_field.get("dimension") != embedding_dimension:
        raise ValueError("Pinecone body_vector dimension does not match the embedding model.")
    text_field = fields.get("body", {})
    if text_field.get("type") != "string" or not text_field.get("store_text", True):
        raise ValueError("Pinecone needs a body string field with stored text enabled.")
