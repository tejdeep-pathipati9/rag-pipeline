"""Combine ten vector and ten keyword candidates while preserving source metadata."""

from pinecone import DenseVectorQuery, TextQuery

TOP_K = 10
# Smooth rank contributions; this is separate from the number of candidates.
RRF_K = 60


def retrieve_dense(question: str, embeddings, index, *, namespace: str) -> list[dict]:
    """Embed a question and return Pinecone's ranked original text and metadata.

    Supply the same embedding model and namespace used for ingestion. MiniLM
    uses the same encoding for documents and questions, so we reuse the existing
    embed_documents() method. Results keep Pinecone's _id, _score and ranking.
    """
    if not question.strip():
        raise ValueError("Question must not be empty.")
    if not namespace.strip():
        raise ValueError("An explicit Pinecone namespace is required.")

    question_vector = embeddings.embed_documents([question])[0]
    response = index.documents.search(
        namespace=namespace,
        top_k=TOP_K,
        score_by=[DenseVectorQuery(values=question_vector, field="body_vector")],
        include_fields=["*"],
    )

    return _extract_hits(response)


def retrieve_hybrid(question: str, embeddings, index, *, namespace: str) -> list[dict]:
    """Retrieve ten candidates per method and return up to twenty unique chunks.

    The existing body field supports keyword search with Pinecone's BM25 ranking.
    Reciprocal rank fusion combines the two lists using positions, because BM25
    and cosine scores have different scales. Source text and metadata stay intact.
    """
    vector_hits = retrieve_dense(question, embeddings, index, namespace=namespace)
    keyword_response = index.documents.search(
        namespace=namespace,
        top_k=TOP_K,
        score_by=[TextQuery(query=question, fields=["body"])],
        include_fields=["*"],
    )
    keyword_hits = _extract_hits(keyword_response)
    return _fuse_results(vector_hits, keyword_hits)


def _extract_hits(response) -> list[dict]:
    """Keep ranked text and metadata, excluding the stored embedding values."""
    results = []
    for match in response.matches:
        hit = match.to_dict()
        hit.pop("body_vector", None)
        results.append(hit)
    return results


def _fuse_results(vector_hits: list[dict], keyword_hits: list[dict]) -> list[dict]:
    """Merge by chunk ID and add rank contributions, preserving each method's score.

    RRF adds 1 / (60 + rank) for each list containing the chunk. A rank of one
    contributes 1/61. This combines rankings without a learned reranking model.
    """
    merged = {}
    for method, hits in (("vector", vector_hits), ("keyword", keyword_hits)):
        for rank, hit in enumerate(hits, start=1):
            chunk_id = hit["_id"]
            if chunk_id not in merged:
                merged[chunk_id] = hit.copy()
                # Replace the unlabelled native score with explicit score fields.
                merged[chunk_id].pop("_score", None)
                merged[chunk_id]["rrf_score"] = 0.0

            result = merged[chunk_id]
            result["rrf_score"] += 1 / (RRF_K + rank)
            result[f"{method}_rank"] = rank
            result[f"{method}_score"] = hit["_score"]

    # Chunk IDs provide a deterministic order when fused scores are equal.
    return sorted(merged.values(), key=lambda hit: (-hit["rrf_score"], hit["_id"]))
