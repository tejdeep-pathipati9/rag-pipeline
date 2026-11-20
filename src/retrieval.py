"""Retrieve vector/keyword candidates and rerank them without changing source records."""

from math import isfinite

from pinecone import DenseVectorQuery, TextQuery
from sentence_transformers import CrossEncoder

TOP_K = 10
# Smooth rank contributions; this is separate from the number of candidates.
RRF_K = 60
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
RERANKER_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"
EVIDENCE_TOKEN_BUDGET = 4000


def assemble_evidence(chunks: list[dict], tokenizer, *, token_budget=EVIDENCE_TOKEN_BUDGET):
    """Expand ranked children to stored source sections, deduplicate and bound context.

    Count source content tokens with the embedding tokenizer, excluding prompt/metadata.
    Scores still describe the selected child. Old namespaces retain child-only evidence.
    """
    if token_budget <= 0:
        raise ValueError("Evidence token budget must be positive.")
    evidence, seen, used = [], set(), 0
    for chunk in chunks:
        record = chunk.copy()
        if "parent_id" in chunk:
            record.update(
                _id=chunk["parent_id"],
                child_id=chunk["_id"],
                body=chunk["parent_body"],
                section_ids=chunk["parent_section_ids"],
                start_char=chunk["parent_start_char"],
                end_char=chunk["parent_end_char"],
            )
        if record["_id"] in seen:
            continue
        tokens = len(tokenizer.encode(record["body"]))
        if used + tokens > token_budget:
            continue
        evidence.append(record)
        seen.add(record["_id"])
        used += tokens
    return evidence


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


def rerank_results(question: str, chunks: list[dict], reranker: CrossEncoder) -> list[dict]:
    """Score each question/text pair, then return all candidates in descending order.

    Load the cross-encoder once in the caller and reuse it. Scores measure model
    relevance, not eligibility or probabilities. Metadata stays out of model input
    but is preserved in the returned records, along with the original RRF scores.
    """
    if not question.strip():
        raise ValueError("Question must not be empty.")
    if not chunks:
        return []

    pairs = [(question, chunk["body"]) for chunk in chunks]
    scores = [float(score) for score in reranker.predict(pairs, show_progress_bar=False)]
    if len(scores) != len(chunks):
        raise ValueError("Reranker must return one score per chunk.")
    if not all(isfinite(score) for score in scores):
        raise ValueError("Reranker scores must be finite.")

    # Copy records so callers can still inspect the unchanged retrieval results.
    results = [
        {**chunk, "rerank_score": score} for chunk, score in zip(chunks, scores, strict=True)
    ]
    # Python's stable sort preserves fused order when model scores are equal.
    return sorted(results, key=lambda hit: hit["rerank_score"], reverse=True)


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
