"""Find candidates, fuse search rankings, rerank, then assemble answer evidence.

Search and reranking operate on embedded child chunks. Evidence assembly can
replace those children with complete parent sections for the answer model.
None of these steps decides whether a policy actually grants a benefit.
"""

from math import isfinite

from pinecone import DenseVectorQuery, TextQuery
from sentence_transformers import CrossEncoder

from src.config import AppConfig

TOP_K = AppConfig.retrieval_k
# RRF uses this constant to soften the difference between nearby rank positions.
RRF_K = 60
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
RERANKER_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"
EVIDENCE_TOKEN_BUDGET = 4000


def assemble_evidence(chunks: list[dict], tokenizer, *, token_budget=EVIDENCE_TOKEN_BUDGET):
    """Return ordered source evidence that fits the supplied content-token budget.

    Pass children in their final relevance order. Parent-child records expand to
    their stored parent body, section IDs and character offsets; other records
    stay as children. Include each resulting source ID at most once.

    Count bodies with the embedding tokenizer, excluding prompt and metadata.
    Skip whole sections that do not fit, then try later entries; never truncate
    a policy section. Returned dictionaries are copies, and relevance scores
    still describe the selected child, whose ID is retained as child_id.
    Raise ValueError for a nonpositive budget; empty input returns an empty list.
    """
    if token_budget <= 0:
        raise ValueError("Evidence token budget must be positive.")
    evidence, seen, used = [], set(), 0
    for chunk in chunks:
        record = chunk.copy()
        if "parent_id" in chunk:
            # Citation offsets must describe the expanded body, not the smaller child.
            record.update(
                _id=chunk["parent_id"],
                child_id=chunk["_id"],
                body=chunk["parent_body"],
                section_ids=chunk["parent_section_ids"],
                start_char=chunk["parent_start_char"],
                end_char=chunk["parent_end_char"],
            )
        if record["_id"] in seen:
            # Several relevant children can point to the same policy chapter.
            continue
        tokens = len(tokenizer.encode(record["body"]))
        if used + tokens > token_budget:
            # A smaller, lower-ranked section may still fit the remaining budget.
            continue
        evidence.append(record)
        seen.add(record["_id"])
        used += tokens
    return evidence


def retrieve_dense(
    question: str, embeddings, index, *, namespace: str, filters=None, top_k: int = TOP_K
) -> list[dict]:
    """Return up to top_k semantic matches from the selected indexed namespace.

    Use the same embedding model and revision as ingestion. MiniLM uses the same
    encoding for questions and documents, so embed_documents() handles both.
    Pinecone ranks against body_vector and returns stored bodies and metadata;
    results retain its native _score and order but omit the vector payload.

    Optional filters are passed to Pinecone unchanged. This function does not
    infer current policy status or effective dates. Raise ValueError for a blank
    question/namespace or nonpositive top_k; model and service errors propagate.
    """
    if not question.strip():
        raise ValueError("Question must not be empty.")
    if not namespace.strip():
        raise ValueError("An explicit Pinecone namespace is required.")
    if top_k <= 0:
        raise ValueError("top_k must be positive.")

    question_vector = embeddings.embed_documents([question])[0]
    response = index.documents.search(
        namespace=namespace,
        top_k=top_k,
        score_by=[DenseVectorQuery(values=question_vector, field="body_vector")],
        include_fields=["*"],
        **({"filter": filters} if filters is not None else {}),
    )

    return _extract_hits(response)


def retrieve_hybrid(
    question: str, embeddings, index, *, namespace: str, filters=None, top_k: int = TOP_K
) -> list[dict]:
    """Combine semantic and BM25 keyword matches using reciprocal rank fusion.

    Search the same namespace and apply the same optional filters to both
    methods. top_k is the candidate limit per method, so the fused result can
    contain up to 2 * top_k unique chunks. It is not a final context limit.

    Keyword search runs on the stored body field. Fusion uses rank positions,
    because native vector and BM25 scores have different scales. Return source
    records in fused order; cross-encoder reranking is a separate caller step.
    """
    vector_hits = retrieve_dense(
        question, embeddings, index, namespace=namespace, filters=filters, top_k=top_k
    )
    # Keyword matching can recover exact policy codes that semantic search ranks low.
    keyword_response = index.documents.search(
        namespace=namespace,
        top_k=top_k,
        score_by=[TextQuery(query=question, fields=["body"])],
        include_fields=["*"],
        **({"filter": filters} if filters is not None else {}),
    )
    keyword_hits = _extract_hits(keyword_response)
    return _fuse_results(vector_hits, keyword_hits)


def rerank_results(question: str, chunks: list[dict], reranker: CrossEncoder) -> list[dict]:
    """Return copies of all candidates sorted by cross-encoder relevance.

    The caller supplies a loaded CrossEncoder so it can be reused across questions.
    Unlike vector search, the model reads the question and body together for each
    candidate. Only body text enters the pair; titles and other metadata do not.

    Add rerank_score while preserving source metadata and earlier search scores.
    Scores express relevance, not probabilities or policy eligibility. Ties keep
    input order, and no top-k cutoff is applied here. Empty candidates return [].
    Raise ValueError for a blank question or missing/non-finite model scores.
    """
    if not question.strip():
        raise ValueError("Question must not be empty.")
    if not chunks:
        return []

    # Rescore each existing candidate; reranking cannot recover an absent chunk.
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
    """Convert SDK matches to dictionaries without changing their search order.

    Keep the native score, source text and metadata. Remove body_vector because
    later ranking, citation display and answer generation do not need its values.
    """
    results = []
    for match in response.matches:
        hit = match.to_dict()
        hit.pop("body_vector", None)
        results.append(hit)
    return results


def _fuse_results(vector_hits: list[dict], keyword_hits: list[dict]) -> list[dict]:
    """Merge matches by _id and return them in reciprocal-rank-fusion order.

    Each occurrence contributes 1 / (RRF_K + its one-based rank). A chunk found
    by both methods accumulates both contributions. Original text and metadata
    come from its first occurrence; method-specific ranks and native scores are
    stored separately so unlike score scales are never added together.

    Return copied records with rrf_score, breaking score ties by chunk ID.
    Empty input lists return []. Fusion does not call a model or select parents.
    """
    merged = {}
    for method, hits in (("vector", vector_hits), ("keyword", keyword_hits)):
        for rank, hit in enumerate(hits, start=1):
            chunk_id = hit["_id"]
            if chunk_id not in merged:
                merged[chunk_id] = hit.copy()
                # An unlabeled _score would hide whether it came from vector or BM25 search.
                merged[chunk_id].pop("_score", None)
                merged[chunk_id]["rrf_score"] = 0.0

            result = merged[chunk_id]
            result["rrf_score"] += 1 / (RRF_K + rank)
            result[f"{method}_rank"] = rank
            result[f"{method}_score"] = hit["_score"]

    # Chunk IDs provide a deterministic order when fused scores are equal.
    return sorted(merged.values(), key=lambda hit: (-hit["rrf_score"], hit["_id"]))
