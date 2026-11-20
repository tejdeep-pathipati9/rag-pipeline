"""Embed prepared chunks and store their text, vectors and metadata in Pinecone."""

import math


def ingest_chunks(chunks, embeddings, index, *, namespace: str, batch_size: int = 64) -> int:
    """Upload prepared chunks in batches and return the number Pinecone acknowledged.

    Each chunk already contains its ID, original body and source metadata.
    Only body is sent to the embedding model. Copying the chunk keeps its
    metadata intact and lets callers reuse it for another run.
    """
    if not namespace.strip():
        raise ValueError("An explicit Pinecone namespace is required.")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive.")

    total = 0
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]

        # Embed the text of each chunk in the same order as the batch.
        texts = [chunk["body"] for chunk in batch]
        vectors = embeddings.embed_documents(texts)
        if len(vectors) != len(batch):
            raise ValueError("The embedding result count does not match the chunk count.")

        # Attach each vector to a copy of its original text and metadata.
        documents = []
        for chunk, vector in zip(batch, vectors, strict=True):
            if len(vector) != embeddings.dimension or not all(
                math.isfinite(value) for value in vector
            ):
                raise ValueError("Invalid embedding dimension or non-finite embedding values.")

            document = chunk.copy()
            document["body_vector"] = vector
            document["embedding_model"] = embeddings.model_name
            document["embedding_revision"] = embeddings.revision
            documents.append(document)

        # Existing IDs are overwritten, so repeating a run does not duplicate them.
        response = index.documents.upsert(namespace=namespace, documents=documents)
        if response.upserted_count != len(documents):
            raise RuntimeError("Pinecone did not acknowledge every chunk in the batch.")
        total += response.upserted_count

    return total


def validate_index(description: dict, embedding_dimension: int) -> None:
    """Check that Pinecone can store the text and the model's vector dimension."""
    fields = description.get("schema", {}).get("fields", {})
    vector_field = fields.get("body_vector", {})
    if vector_field.get("type") != "dense_vector":
        raise ValueError("Pinecone needs a body_vector dense_vector field.")
    if vector_field.get("dimension") != embedding_dimension:
        raise ValueError("Pinecone body_vector dimension does not match the embedding model.")
    text_field = fields.get("body", {})
    if text_field.get("type") != "string" or not text_field.get("store_text", True):
        raise ValueError("Pinecone needs a body string field with stored text enabled.")
