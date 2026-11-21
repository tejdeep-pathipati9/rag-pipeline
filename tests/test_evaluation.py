"""Check fifteen fixed policy questions, real source sections and evaluation math offline."""

import json
import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import pytest

from scripts import evaluate as runner
from scripts.evaluate import load_cases, score_case
from src import config as config_module
from src.documents import _section_ranges, load_document

CASES = load_cases()
ANSWERS = [
    (
        "Weather and other uncontrollable disruptions qualify for rebooking at no additional fare, "
        "subject to seat availability."
    ),
    (
        "An offer does not mean the flight is confirmed. "
        "A replacement reservation must be accepted and ticketed."
    ),
    (
        "A valid Northstar disrupted itinerary, final approved airline-controlled cause, "
        "overnight need and a station away from home must all hold."
    ),
    "Weather and external ATC delays are not covered by the standard hotel commitment.",
    (
        "Finalized crew scheduling is included in 2026, with overnight necessity "
        "and a station away from home still required."
    ),
    (
        "Arrival at the final destination at least three hours later meets the threshold. "
        "Decline the replacement and do not use the alternative transportation."
    ),
    (
        "No full refund is available under this remedy for transportation already used "
        "after the replacement was flown."
    ),
    "The latest authorized, signed final investigation supersedes preliminary gate comments.",
    "Separate tickets are outside the protected connection policy.",
    "A passenger in their home city is not eligible for the standard overnight hotel.",
    "Obtain written approval before booking, including the maximum reimbursable rate.",
    "You remain eligible; room availability is a fulfillment problem that the agent must escalate.",
    "Hotel eligibility is pending until the final approved cause classification is confirmed.",
    (
        "Not automatically. A qualifying cancellation or significant change and the passenger's "
        "choice to decline unused travel must be assessed."
    ),
    (
        "Last year was 2025. Crew scheduling was excluded from that older policy's "
        "routine hotel benefit."
    ),
]


def test_evaluation_has_fifteen_policy_questions_and_no_passenger_records():
    assert len(CASES) == 15
    assert all(c["case_id"].startswith("POL-") for c in CASES)
    assert all(not re.search(r"\b20\d{2}\b|NS-[A-Z]+-", c["question"]) for c in CASES)


@pytest.mark.parametrize(
    ("case", "text"), list(zip(CASES, ANSWERS, strict=True)), ids=[c["case_id"] for c in CASES]
)
def test_fixed_policy_answers_and_source_recall(case, text):
    sources = {}
    for path in Path("corpus/policies").glob("*.md"):
        metadata, body = load_document(path, Path("corpus"))
        for section, start, end in _section_ranges(body):
            sources[f"{metadata['document_id']}#{section}"] = body[start:end]
    hits = []
    for ref in case["expected_sections"]:
        assert ref in sources
        doc, section = ref.split("#")
        hits.append({"document_id": doc, "section_ids": [section], "body": sources[ref]})
    assert all(ref in sources for path in case.get("citation_paths", []) for ref in path)
    answer = {"answer": text, "citations": case["expected_sections"], "missing_information": []}
    scores = score_case(case, hits, answer)
    assert scores["section_recall_at_5"] == 1
    assert scores["answer_pass"]
    assert not score_case(case, hits, {**answer, "answer": "Ask support."})["answer_pass"]
    assert not score_case(case, hits, {**answer, "citations": ["INVENTED#1"]})["answer_pass"]


def test_recall_counts_all_gold_sections_and_distinguishes_top_five():
    case = {"expected_sections": ["P#1", "P#2"], "expected_facts": {"threshold": ["three hours"]}}
    hits = [{"document_id": "P", "section_ids": ["1"]}]
    hits += [{"document_id": "OTHER", "section_ids": [str(i)]} for i in range(4)]
    hits += [{"document_id": "P", "section_ids": ["2"]}]
    scores = score_case(case, hits, None)
    assert scores["section_recall_at_5"] == 0.5
    assert scores["section_recall_in_context"] == 1
    assert not scores["answer_pass"]


def test_equivalent_citations_require_the_whole_supporting_path():
    case = {
        "expected_sections": ["CARE#4.5"],
        "expected_facts": {"crew coverage": ["crew is included"]},
        "citation_paths": [["CARE#4.5"], ["CARE#1.2", "CARE#4.1"]],
    }
    hits = [{"document_id": "CARE", "section_ids": ["1.2", "4.1"]}]
    answer = {"answer": "Crew is included.", "citations": ["CARE#1.2"]}
    assert not score_case(case, hits, answer)["answer_pass"]
    answer["citations"].append("CARE#4.1")
    scores = score_case(case, hits, answer)
    assert scores["answer_pass"]
    assert scores["section_recall_in_context"] == 0  # Canonical section was not retrieved.


def test_ranked_recall_at_five_and_ten_use_different_cutoffs(monkeypatch, tmp_path, tokenizer):
    monkeypatch.chdir(tmp_path)
    case = {"case_id": "cutoffs", "question": "Hotel?", "expected_sections": ["P#1", "P#2"],
            "expected_facts": {}}
    hits = [{"_id": str(i), "document_id": "OTHER", "section_ids": ["1"], "body": "Policy"}
            for i in range(11)]
    hits[5].update(document_id="P", section_ids=["1"])
    hits[10].update(document_id="P", section_ids=["2"])
    monkeypatch.setattr(runner, "retrieve_hybrid", Mock(return_value=hits))
    monkeypatch.setattr(runner, "rerank_results", Mock(return_value=hits))

    summary = runner.evaluate_cases(
        [case], SimpleNamespace(tokenizer=tokenizer), object(), object(), None,
        namespace="test", model="unused", retrieval_only=True,
    )

    assert summary["ranked_chunk_recall_at_5"] == 0
    assert summary["ranked_chunk_recall_at_10"] == 0.5  # Rank 11 is excluded.
    assert summary["retrieval_recall_in_context"] == 1
    report = runner.RESULTS_FILE.with_suffix(".md").read_text()
    assert "Ranked chunk recall@10: **50.0%**" in report


def test_evaluation_records_real_context_and_provider_failures(monkeypatch, tmp_path, tokenizer):
    expected = {"expected_sections": ["CARE#4.1"], "expected_facts": {"overnight": ["overnight"]}}
    cases = [
        {"case_id": name, "question": "Hotel policy?", **expected}
        for name in ["complete", "failed"]
    ]
    monkeypatch.chdir(tmp_path)
    child = {
        "_id": "child",
        "body": "Hotel",
        "document_id": "CARE",
        "section_ids": ["4"],
        "parent_id": "parent",
        "parent_body": "Hotel requires an overnight stay",
        "parent_start_char": 0,
        "parent_end_char": 32,
        "parent_section_ids": ["4", "4.1"],
    }
    monkeypatch.setattr(runner, "retrieve_hybrid", Mock(return_value=[child]))
    answer = {
        "answer": "An overnight stay is required.",
        "citations": ["CARE#4.1"],
        "missing_information": [],
    }
    generate = Mock(
        side_effect=[Mock(model_dump=Mock(return_value=answer)), RuntimeError("Provider details")]
    )
    monkeypatch.setattr(runner, "generate_answer", generate)
    model = SimpleNamespace(model_name="test", revision="test", tokenizer=tokenizer)
    reranker = SimpleNamespace(predict=Mock(return_value=[0.9]))
    summary = runner.evaluate_cases(
        cases, model, object(), reranker, object(), namespace="test", model="test"
    )
    assert summary["errors"] == 1
    assert summary["answer_check_pass_rate"] == 0.5
    assert summary["retrieval_recall_at_5"] == 1
    assert summary["ranked_chunk_recall_at_5"] == 0  # Parent expansion is not better child ranking.
    results = json.loads(runner.RESULTS_FILE.read_text())
    assert results["summary"] == summary
    completed, failed = results["cases"]
    assert completed["matches"][0]["child_id"] == "child"
    assert generate.call_args_list[0].args[1] == completed["matches"]
    assert generate.call_args_list[0].kwargs["as_of"] == runner.EVALUATION_DATE
    assert results["as_of_date"] == runner.EVALUATION_DATE
    assert failed["error"] == "RuntimeError"
    assert "Provider details" not in runner.RESULTS_FILE.read_text()
    assert list(Path("artifacts").rglob("*.json")) == [runner.RESULTS_FILE]
    report = runner.RESULTS_FILE.with_suffix(".md").read_text()
    assert "# Policy Q&A evaluation" in report
    assert "PASS" in report and "FAIL" in report
    assert "An overnight stay is required." in report
    assert "Hotel requires an overnight stay" not in report  # Full chunk bodies stay in JSON.


def test_retrieval_only_does_not_generate_answers_or_report_zero_accuracy(
    monkeypatch, tmp_path, tokenizer
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(runner, "retrieve_hybrid", Mock(return_value=[]))
    generate = Mock()
    monkeypatch.setattr(runner, "generate_answer", generate)
    embeddings, index = SimpleNamespace(tokenizer=tokenizer), object()
    summary = runner.evaluate_cases(
        CASES[:1], embeddings, index, object(), None,
        namespace="test", model="unused", top_k=20, retrieval_only=True,
    )
    generate.assert_not_called()
    assert summary["answer_check_pass_rate"] is None
    runner.retrieve_hybrid.assert_called_once_with(
        CASES[0]["question"], embeddings, index, namespace="test", top_k=20,
    )
    assert "Not run (retrieval only)" in runner.RESULTS_FILE.with_suffix(".md").read_text()


@pytest.mark.parametrize("search", ["dense", "hybrid"])
def test_evaluation_search_mode_uses_only_the_selected_retriever(
    monkeypatch, tmp_path, tokenizer, search
):
    monkeypatch.chdir(tmp_path)
    dense, hybrid = Mock(return_value=[]), Mock(return_value=[])
    monkeypatch.setattr(runner, "retrieve_dense", dense)
    monkeypatch.setattr(runner, "retrieve_hybrid", hybrid)
    monkeypatch.setattr(runner, "rerank_results", Mock(return_value=[]))
    embeddings, index = SimpleNamespace(tokenizer=tokenizer), object()
    runner.evaluate_cases(
        CASES[:1], embeddings, index, object(), None, namespace="test", model="",
        retrieval_only=True, search=search,
    )
    selected, unused = (dense, hybrid) if search == "dense" else (hybrid, dense)
    selected.assert_called_once_with(
        CASES[0]["question"], embeddings, index, namespace="test", top_k=20,
    )
    unused.assert_not_called()
    result = json.loads(runner.RESULTS_FILE.read_text())
    assert result["search"] == search
    assert f"Search: **{search}**" in runner.render_report(result)


@pytest.mark.parametrize(
    ("questions_error", "message"),
    [(True, "Cannot load evaluation questions"), (False, "LLM_API_KEY")],
)
def test_evaluation_configuration_errors_before_loading_models(
    monkeypatch, capsys, questions_error, message
):
    load_model = Mock()
    monkeypatch.setattr(runner, "EmbeddingModel", load_model)
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    if questions_error:
        monkeypatch.setattr(runner, "load_cases", Mock(side_effect=ValueError("No questions")))

    with pytest.raises(SystemExit) as error:
        runner.main([])

    assert error.value.code == 2
    assert message in capsys.readouterr().err
    load_model.assert_not_called()


@pytest.mark.parametrize("errors", [0, 1])
@pytest.mark.parametrize("retrieval_only", [False, True])
def test_evaluation_cli_reports_summary_and_exits_nonzero_for_failed_cases(
    monkeypatch, capsys, errors, retrieval_only
):
    embeddings = SimpleNamespace(model_name="test", revision="test", dimension=384)
    monkeypatch.setattr(config_module, "load_dotenv", Mock())
    monkeypatch.setattr(runner, "EmbeddingModel", Mock(return_value=embeddings))
    monkeypatch.setattr(runner, "validate_index", Mock())
    pinecone = MagicMock()
    pinecone.__enter__.return_value = pinecone
    pinecone.describe_index.return_value.to_dict.return_value = {"host": "https://test-index"}
    monkeypatch.setattr(runner, "Pinecone", Mock(return_value=pinecone))
    reranker = Mock()
    monkeypatch.setattr(runner, "CrossEncoder", Mock(return_value=reranker))
    foundry = MagicMock()
    monkeypatch.setattr(runner, "AnthropicFoundry", foundry)
    for key in ("PINECONE_API_KEY", "PINECONE_INDEX_NAME", "LLM_API_KEY", "LLM_BASE_URL"):
        monkeypatch.setenv(key, "test")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    if retrieval_only:
        for key in ("LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"):
            monkeypatch.delenv(key, raising=False)
    evaluate = Mock(return_value={"errors": errors})
    monkeypatch.setattr(runner, "evaluate_cases", evaluate)
    arguments = ["--namespace", "test"]
    if retrieval_only:
        arguments.extend(["--retrieval-only", "--top-k", "20"])

    if errors:
        with pytest.raises(SystemExit) as error:
            runner.main(arguments)
        assert error.value.code == 1
    else:
        runner.main(arguments)

    assert json.loads(capsys.readouterr().out) == {"errors": errors}
    cases, model, connected_index, loaded_reranker, client = evaluate.call_args.args
    assert cases == CASES
    assert (model, connected_index, loaded_reranker, client) == (
        embeddings,
        pinecone.Index.return_value.__enter__.return_value,
        reranker,
        None if retrieval_only else foundry.return_value.__enter__.return_value,
    )
    assert evaluate.call_args.kwargs == {
        "namespace": "test", "model": "" if retrieval_only else "test-model",
        "top_k": 20, "retrieval_only": retrieval_only,
        "search": "hybrid",
    }
    if retrieval_only:
        foundry.assert_not_called()
