"""Run the policy benchmark: python -m scripts.evaluate."""

import argparse
import json
import re
from contextlib import nullcontext
from html import escape
from pathlib import Path

from anthropic import AnthropicFoundry, APIError
from pinecone import NotFoundError, Pinecone
from pinecone.errors import PineconeError
from sentence_transformers import CrossEncoder

from src.config import AppConfig
from src.embedding import EmbeddingModel
from src.ingestion import validate_index
from src.model import generate_answer
from src.retrieval import (
    RERANKER_MODEL,
    RERANKER_REVISION,
    TOP_K,
    assemble_evidence,
    rerank_results,
    retrieve_hybrid,
)

GOLD_SET = Path("evaluation/flight_disruption_gold_set.jsonl")
# Freeze the reference date so "last year" has the same meaning in every benchmark run.
EVALUATION_DATE = "2026-11-20"
RESULTS_FILE = Path("artifacts/evaluation.json")


def load_cases() -> list[dict]:
    cases = [json.loads(line) for line in GOLD_SET.read_text().splitlines() if line.strip()]
    if not cases:
        raise ValueError("The benchmark has no questions.")
    return cases


def _normalized(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip() + " "


def score_case(case: dict, hits: list[dict], answer: dict | None) -> dict:
    """Measure section-ID recall and explicit phrase groups; this is not semantic grading."""
    refs = [{f"{h['document_id']}#{s}" for s in h["section_ids"]} for h in hits]
    top_five = set().union(*refs[:5])
    context = set().union(*refs)
    gold = set(case["expected_sections"])
    text = _normalized(answer["answer"]) if answer else " "
    facts = {
        name: any(_normalized(phrase) in text for phrase in alternatives)
        for name, alternatives in case["expected_facts"].items()
    }
    citations = set(answer["citations"]) if answer else set()
    citation_paths = case.get("citation_paths", [[ref] for ref in gold])
    return {
        "section_recall_at_5": len(gold & top_five) / len(gold),
        "section_recall_in_context": len(gold & context) / len(gold),
        "key_facts": facts,
        "key_information_pass": bool(answer) and all(facts.values()),
        "citation_ids_valid": bool(citations) and citations <= context,
        "answer_pass": bool(answer)
        and all(facts.values())
        and any(set(path) <= citations for path in citation_paths)
        and citations <= context,
    }


def render_report(results: dict) -> str:
    """Show the comparison metrics and answers without dumping retrieved chunk bodies."""
    summary = results["summary"]
    accuracy = summary["answer_accuracy"]
    pool_recall = summary.get("candidate_recall")
    chunk_recall = summary.get("ranked_chunk_recall_at_5")
    chunk_recall_ten = summary.get("ranked_chunk_recall_at_10")
    notes = {note["case_id"]: note["finding"] for note in results.get("review_notes", [])}
    lines = [
        "# Policy Q&A evaluation",
        "",
        f"Namespace: `{results['namespace']}` · Candidates per search: **{results['top_k']}**",
        f"Reference date: {results['as_of_date']} · Questions: {summary['cases']} "
        f"· Service errors: {summary['errors']}",
        "",
        f"- Candidate pool recall: **{pool_recall:.1%}**"
        if pool_recall is not None
        else "- Candidate pool recall: Not recorded",
        f"- Ranked chunk recall@5: **{chunk_recall:.1%}**"
        if chunk_recall is not None
        else "- Ranked chunk recall@5: Not recorded",
        f"- Ranked chunk recall@10: **{chunk_recall_ten:.1%}**"
        if chunk_recall_ten is not None
        else "- Ranked chunk recall@10: Not recorded",
        f"- First-five context-entry recall: **{summary['retrieval_recall_at_5']:.1%}**",
        f"- Final context recall: **{summary['retrieval_recall_in_context']:.1%}**",
        f"- Answer checks: **{accuracy:.1%}**"
        if accuracy is not None
        else "- Answer checks: **Not run (retrieval only)**",
        "",
        "Recall uses the listed gold sections. Accepted equivalent clauses may also support "
        "an answer. Parent expansion creates larger context entries; their recall@5 is not "
        "a chunk-ranking score. Section IDs alone do not prove a complete clause was provided.",
        "",
        "| Question | Pool recall | Chunk recall@5 | Chunk recall@10 | Context | Answer check |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for record in results["cases"]:
        scores = record["scores"]
        status = (
            "Not run"
            if results["retrieval_only"]
            else ("PASS" if scores["answer_pass"] else "FAIL")
        )
        question = record["question"].replace("|", "\\|").replace("\n", " ")
        pool = record.get("candidate_recall")
        pool_label = "Not recorded" if pool is None else f"{pool:.0%}"
        ranked = record.get("ranked_chunk_recall_at_5")
        ranked_label = "Not recorded" if ranked is None else f"{ranked:.0%}"
        ranked_ten = record.get("ranked_chunk_recall_at_10")
        ten_label = "Not recorded" if ranked_ten is None else f"{ranked_ten:.0%}"
        lines.append(
            f"| {record['case_id']}: {question} | "
            f"{pool_label} | "
            f"{ranked_label} | "
            f"{ten_label} | "
            f"{scores['section_recall_in_context']:.0%} | {status} |"
        )
    lines.extend(["", "## Questions", "", "Expand a question to inspect its answer and gaps.", ""])
    for record in results["cases"]:
        missing_facts = [name for name, ok in record["scores"]["key_facts"].items() if not ok]
        missing_sections = ", ".join(record["missing_sections"]) or "None"
        lines.extend(
            [
                f"<details><summary>{record['case_id']}: {escape(record['question'])}</summary>",
                "",
                record["question"],
                "",
                f"**Missing gold sections in context:** {missing_sections}",
                "",
            ]
        )
        if record.get("error"):
            lines.extend([f"**Service error:** {record['error']}", ""])
        if record["case_id"] in notes:
            lines.extend([f"**Review note:** {notes[record['case_id']]}", ""])
        if record["answer"]:
            lines.extend(
                [
                    f"**Missing expected information:** {', '.join(missing_facts) or 'None'}",
                    "",
                    record["answer"]["answer"],
                    "",
                    f"**Citations:** {', '.join(record['answer']['citations']) or 'None'}",
                ]
            )
        lines.extend(["", "</details>", ""])
    return "\n".join(lines)


def evaluate_cases(
    cases,
    embeddings,
    index,
    reranker,
    client,
    *,
    namespace,
    model,
    top_k: int = TOP_K,
    retrieval_only: bool = False,
) -> dict:
    records = []
    for case in cases:
        record = {
            "case_id": case["case_id"],
            "question": case["question"],
            "matches": [],
            "answer": None,
            "candidate_recall": 0.0,
            "ranked_chunk_recall_at_5": 0.0,
            "ranked_chunk_recall_at_10": 0.0,
        }
        try:
            candidates = retrieve_hybrid(
                case["question"], embeddings, index, namespace=namespace, top_k=top_k
            )
            record["candidate_recall"] = score_case(case, candidates, None)[
                "section_recall_in_context"
            ]
            ranked = rerank_results(case["question"], candidates, reranker)
            record["ranked_chunk_recall_at_5"] = score_case(case, ranked, None)[
                "section_recall_at_5"
            ]
            record["ranked_chunk_recall_at_10"] = score_case(case, ranked[:10], None)[
                "section_recall_in_context"
            ]
            record["matches"] = assemble_evidence(ranked, embeddings.tokenizer)
            if not retrieval_only:
                record["answer"] = generate_answer(
                    case["question"], record["matches"], client, model=model, as_of=EVALUATION_DATE
                ).model_dump()
        except (APIError, PineconeError, ValueError, RuntimeError) as error:
            record["error"] = type(error).__name__
        record["scores"] = score_case(case, record["matches"], record["answer"])
        found = {
            f"{hit['document_id']}#{section}"
            for hit in record["matches"]
            for section in hit["section_ids"]
        }
        record["missing_sections"] = sorted(set(case["expected_sections"]) - found)
        records.append(record)
    summary = {
        "cases": len(records),
        "errors": sum("error" in r for r in records),
        "candidate_recall": sum(r["candidate_recall"] for r in records) / len(records),
        "ranked_chunk_recall_at_5": sum(r["ranked_chunk_recall_at_5"] for r in records)
        / len(records),
        "ranked_chunk_recall_at_10": sum(r["ranked_chunk_recall_at_10"] for r in records)
        / len(records),
        "retrieval_recall_at_5": sum(r["scores"]["section_recall_at_5"] for r in records)
        / len(records),
        "retrieval_recall_in_context": sum(
            r["scores"]["section_recall_in_context"] for r in records
        )
        / len(records),
        "answer_accuracy": None
        if retrieval_only
        else sum(r["scores"]["answer_pass"] for r in records) / len(records),
    }
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    results = {
        "namespace": namespace,
        "model": model,
        "as_of_date": EVALUATION_DATE,
        "top_k": top_k,
        "retrieval_only": retrieval_only,
        "summary": summary,
        "cases": records,
    }
    RESULTS_FILE.write_text(json.dumps(results, indent=2) + "\n")
    RESULTS_FILE.with_suffix(".md").write_text(render_report(results))
    return summary


def main(argv=None):
    config = AppConfig.from_env()
    parser = argparse.ArgumentParser(description="Run the fixed policy question benchmark.")
    parser.add_argument("--namespace", default=config.namespace)
    parser.add_argument(
        "--top-k",
        type=int,
        default=config.retrieval_k,
        help="Candidates from each search method (not the recall@5 cutoff).",
    )
    parser.add_argument(
        "--retrieval-only", action="store_true", help="Skip paid answer generation."
    )
    args = parser.parse_args(argv)
    if args.top_k <= 0:
        parser.error("--top-k must be positive.")
    try:
        cases = load_cases()
    except (OSError, ValueError) as error:
        parser.error(f"Cannot load evaluation questions: {error}")

    try:
        config.validate(require_index=True, require_llm=not args.retrieval_only)
    except ValueError as error:
        parser.error(str(error))
    embeddings = EmbeddingModel(
        config.embedding_model,
        revision=config.embedding_revision,
        cache_dir=config.cache_dir,
    )
    with Pinecone(api_key=config.pinecone_api_key) as client:
        try:
            description = client.describe_index(config.pinecone_index_name).to_dict()
        except NotFoundError:
            parser.error("Index not found. Check PINECONE_INDEX_NAME and PINECONE_API_KEY.")
        validate_index(description, embeddings.dimension)
        reranker = CrossEncoder(
            RERANKER_MODEL,
            revision=RERANKER_REVISION,
            cache_folder=config.cache_dir,
            device="cpu",
        )
        llm_context = (
            nullcontext(None)
            if args.retrieval_only
            else AnthropicFoundry(
                api_key=config.llm_api_key, base_url=config.llm_base_url, timeout=120.0
            )
        )
        with client.Index(host=description["host"]) as index, llm_context as llm:
            summary = evaluate_cases(
                cases,
                embeddings,
                index,
                reranker,
                llm,
                namespace=args.namespace,
                model=config.llm_model,
                top_k=args.top_k,
                retrieval_only=args.retrieval_only,
            )
    print(json.dumps(summary, indent=2))
    if summary["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
