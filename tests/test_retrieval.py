"""Check the question-to-Pinecone pipeline without model downloads or network calls."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from sentence_transformers import CrossEncoder

from src.retrieval import _fuse_results, rerank_results, retrieve_dense, retrieve_hybrid


@pytest.fixture
def embeddings():
    """Stand in for the same configured model used during ingestion."""
    return SimpleNamespace(embed_documents=Mock(return_value=[[0.1, 0.2, 0.3]]))


def test_vector_retrieval_embeds_question_and_searches_top_10_in_selected_namespace(embeddings):
    """Use the query vector for dense search, requesting text and source metadata."""
    search = Mock(return_value=SimpleNamespace(matches=[]))
    index = SimpleNamespace(documents=SimpleNamespace(search=search))

    assert (
        retrieve_dense("Am I eligible for a hotel?", embeddings, index, namespace="recursive-test")
        == []
    )

    embeddings.embed_documents.assert_called_once_with(["Am I eligible for a hotel?"])
    request = search.call_args.kwargs
    assert request["namespace"] == "recursive-test"
    assert request["top_k"] == 10
    assert request["include_fields"] == ["*"]
    assert len(request["score_by"]) == 1
    assert request["score_by"][0].field == "body_vector"
    assert request["score_by"][0].values == [0.1, 0.2, 0.3]


def test_retrieval_preserves_ranking_original_text_and_all_metadata(embeddings):
    """Results stay in Pinecone order and retain evidence for later citation/reranking."""
    first = {
        "_id": "chunk-1",
        "_score": 0.9,
        "body": "Original Hotel Text.",
        "document_id": "NS-CARE-2026",
        "document_type": "policy",
        "section_ids": ["4", "4.1"],
        "title": "Passenger Care",
        "version": "2.0",
        "effective_from": "2026-01-01",
        "effective_to": "2026-12-31",
        "status": "current",
        "source_path": "corpus/policies/care.md",
        "chunk_strategy": "recursive",
        "start_char": 25,
        "end_char": 45,
        "source_kind": "synthetic",
        "body_vector": [0.1, 0.2, 0.3],
    }
    second = {**first, "_id": "chunk-2", "_score": 0.8, "status": "superseded"}
    matches = [
        SimpleNamespace(to_dict=lambda record=record: record.copy()) for record in (first, second)
    ]
    index = SimpleNamespace(
        documents=SimpleNamespace(search=Mock(return_value=SimpleNamespace(matches=matches)))
    )

    results = retrieve_dense("Hotel rules?", embeddings, index, namespace="recursive-test")

    assert results == [
        {key: value for key, value in record.items() if key != "body_vector"}
        for record in (first, second)
    ]
    assert "body_vector" in first


@pytest.mark.parametrize(
    ("question", "namespace"), [("", "test"), (" \n", "test"), ("Hotel?", " ")]
)
@pytest.mark.parametrize("retriever", [retrieve_dense, retrieve_hybrid])
def test_empty_question_or_namespace_fails_before_model_or_search(
    embeddings, question, namespace, retriever
):
    """An empty request should not produce an embedding or query the wrong namespace."""
    index = SimpleNamespace(documents=SimpleNamespace(search=Mock()))
    with pytest.raises(ValueError):
        retriever(question, embeddings, index, namespace=namespace)
    embeddings.embed_documents.assert_not_called()
    index.documents.search.assert_not_called()


@pytest.mark.parametrize("top_k", [10, 20])
def test_hybrid_search_passes_candidate_limit_to_both_search_methods(embeddings, top_k):
    """Run two independent ranking methods against the same indexed namespace."""
    search = Mock(return_value=SimpleNamespace(matches=[]))
    index = SimpleNamespace(documents=SimpleNamespace(search=search))

    assert retrieve_hybrid(
        "Hotel accommodation?", embeddings, index, namespace="test", top_k=top_k
    ) == []

    assert search.call_count == 2
    vector_request, keyword_request = [call.kwargs for call in search.call_args_list]
    for request in (vector_request, keyword_request):
        assert request["top_k"] == top_k
        assert request["namespace"] == "test"
        assert request["include_fields"] == ["*"]
    assert vector_request["score_by"][0].values == [0.1, 0.2, 0.3]
    assert vector_request["score_by"][0].field == "body_vector"
    assert keyword_request["score_by"][0].query == "Hotel accommodation?"
    assert keyword_request["score_by"][0].fields == ["body"]
    embeddings.embed_documents.assert_called_once()


def test_policy_filter_applies_identically_to_both_search_channels(embeddings):
    search = Mock(return_value=SimpleNamespace(matches=[]))
    index = SimpleNamespace(documents=SimpleNamespace(search=search))
    filters = {"document_type": {"$eq": "policy"}, "status": {"$eq": "current"}}
    retrieve_hybrid("Crew hotel coverage?", embeddings, index, namespace="test", filters=filters)
    assert len(search.call_args_list) == 2
    assert all(call.kwargs["filter"] == filters for call in search.call_args_list)


def test_fusion_deduplicates_chunks_and_preserves_both_retrieval_scores():
    """A chunk found by both methods appears once and receives both rank contributions."""
    a = {"_id": "a", "_score": 0.9, "body": "First passage.", "section_ids": ["1"]}
    b = {"_id": "b", "_score": 0.8, "body": "Shared passage.", "section_ids": ["2", "2.1"]}
    keyword_b = {**b, "_score": 12.0}
    c = {"_id": "c", "_score": 5.0, "body": "Keyword passage.", "section_ids": ["3"]}

    results = _fuse_results([a, b], [keyword_b, c])

    assert [hit["_id"] for hit in results] == ["b", "a", "c"]
    shared = results[0]
    assert shared["rrf_score"] == pytest.approx(1 / 62 + 1 / 61)
    assert shared["vector_rank"] == 2
    assert shared["vector_score"] == 0.8
    assert shared["keyword_rank"] == 1
    assert shared["keyword_score"] == 12.0
    assert shared["body"] == b["body"]
    assert shared["section_ids"] == ["2", "2.1"]
    assert "_score" not in shared
    assert b["_score"] == 0.8


@pytest.mark.parametrize("empty_method", ["vector", "keyword"])
def test_fusion_keeps_results_when_one_method_finds_nothing(empty_method):
    """An empty keyword or vector list must not discard the other method's candidates."""
    hit = {"_id": "only", "_score": 0.5, "body": "Original text.", "document_id": "POLICY"}
    vector_hits = [] if empty_method == "vector" else [hit]
    keyword_hits = [] if empty_method == "keyword" else [hit]

    results = _fuse_results(vector_hits, keyword_hits)

    assert len(results) == 1
    assert results[0]["_id"] == "only"
    assert results[0]["document_id"] == "POLICY"
    assert results[0]["rrf_score"] == pytest.approx(1 / 61)


def test_fusion_ties_have_a_deterministic_order():
    """Equal rank contributions use the chunk ID as a stable tie-break."""
    vector = [{"_id": "z", "_score": 0.9, "body": "Vector text."}]
    keyword = [{"_id": "a", "_score": 15.0, "body": "Keyword text."}]
    assert [hit["_id"] for hit in _fuse_results(vector, keyword)] == ["a", "z"]


def test_reranker_scores_question_text_pairs_and_preserves_source_records():
    """Only question/text pairs enter the model; all source and retrieval fields survive."""
    chunks = [
        {
            "_id": "case",
            "body": "A historical hotel example.",
            "document_id": "CASE-1",
            "document_type": "historical_case",
            "section_ids": ["1", "1.1"],
            "title": "Historical case",
            "version": "1.0",
            "effective_from": "2025-01-01",
            "effective_to": "2025-12-31",
            "status": "superseded",
            "source_path": "corpus/cases/example.md",
            "chunk_strategy": "recursive",
            "rrf_score": 0.03,
            "vector_rank": 1,
            "vector_score": 0.9,
        },
        {
            "_id": "policy",
            "body": "The passenger care policy covers overnight stays.",
            "document_id": "NS-CARE-2026",
            "section_ids": ["4.1"],
            "rrf_score": 0.02,
            "keyword_rank": 2,
            "keyword_score": 8.0,
        },
    ]
    reranker = Mock(spec=CrossEncoder)
    reranker.predict.return_value = [-2.0, 4.0]

    results = rerank_results("Hotel rules?", chunks, reranker)

    reranker.predict.assert_called_once_with(
        [("Hotel rules?", chunk["body"]) for chunk in chunks], show_progress_bar=False
    )
    assert results == [
        {**chunks[1], "rerank_score": 4.0},
        {**chunks[0], "rerank_score": -2.0},
    ]
    assert all("rerank_score" not in chunk for chunk in chunks)


def test_reranker_keeps_fused_order_when_scores_tie():
    chunks = [{"_id": "z", "body": "First."}, {"_id": "a", "body": "Second."}]
    reranker = Mock(spec=CrossEncoder)
    reranker.predict.return_value = [0.5, 0.5]
    assert [hit["_id"] for hit in rerank_results("Question?", chunks, reranker)] == ["z", "a"]


def test_reranker_skips_model_when_no_candidates_were_retrieved():
    reranker = Mock(spec=CrossEncoder)
    assert rerank_results("Hotel rules?", [], reranker) == []
    reranker.predict.assert_not_called()


def test_reranker_rejects_blank_question_before_scoring():
    reranker = Mock(spec=CrossEncoder)
    with pytest.raises(ValueError, match="Question"):
        rerank_results(" ", [{"_id": "a", "body": "Text."}], reranker)
    reranker.predict.assert_not_called()


@pytest.mark.parametrize("scores", [[], [0.5, 0.6], [float("nan")], [float("inf")]])
def test_reranker_rejects_incomplete_or_nonfinite_scores(scores):
    """A malformed model response must not silently drop chunks or corrupt ordering."""
    reranker = Mock(spec=CrossEncoder)
    reranker.predict.return_value = scores
    with pytest.raises(ValueError, match="score"):
        rerank_results("Hotel rules?", [{"_id": "a", "body": "Text."}], reranker)
