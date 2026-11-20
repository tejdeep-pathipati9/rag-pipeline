"""Replay the active benchmark and score retrieval and decision labels separately."""

import json
from hashlib import sha256
from pathlib import Path
from tempfile import mkdtemp
from time import perf_counter

from anthropic import APIError
from pinecone.errors import PineconeError

from src.model import generate_answer
from src.retrieval import (
    EVIDENCE_TOKEN_BUDGET,
    RERANKER_MODEL,
    RERANKER_REVISION,
    assemble_evidence,
    rerank_results,
    retrieve_hybrid,
)

GOLD_SET = Path("evaluation/flight_disruption_gold_set.jsonl")
# A fixed scenario date makes relative wording repeatable across runs.
SCENARIO_CONTEXT = (
    "Scenario context: The passenger is speaking to Northstar support. "
    "Assume travel in 2026 unless the passenger specifies a different date, "
    "and interpret relative dates as of November 20, 2026. "
    "An explicit travel date or decision time takes precedence."
)


def select_cases(split: str, case_ids: list[str]) -> list[dict]:
    """Select cases within an explicit split, preserving their dataset order."""
    rows = [json.loads(line) for line in GOLD_SET.read_text().splitlines() if line.strip()]
    cases = [row for row in rows if row["split"] == split]
    unknown = sorted(set(case_ids) - {row["case_id"] for row in cases})
    if unknown:
        raise ValueError(f"Cases outside the {split} split: {', '.join(unknown)}.")
    selected = [row for row in cases if not case_ids or row["case_id"] in case_ids]
    if not selected:
        raise ValueError(f"The benchmark has no {split} cases.")
    return selected


def score_case(case: dict, hits: list[dict], answer: dict | None) -> dict:
    """Count evidence paths by section overlap and grade only the requested decisions."""
    refs = [{f"{hit['document_id']}#{section}" for section in hit["section_ids"]} for hit in hits]
    top_five = set().union(*refs[:5])
    context = set().union(*refs)
    decisions = {}
    for benefit, label in case["expected"].items():
        status = answer[benefit]["status"] if answer is not None else None
        claims = label["required"]
        decisions[benefit] = {
            "expected": label["status"],
            "actual": status,
            "exact": status == label["status"],
            "requires_compatibility_review": bool(
                status and status == label.get("compatible_status")
            ),
            "claims": len(claims),
            "claims_at_5": sum(
                any(set(path) <= top_five for path in paths) for paths in claims.values()
            ),
            "missing_context_claims": [
                name
                for name, paths in claims.items()
                if not any(set(path) <= context for path in paths)
            ],
        }
    required_sections = {
        ref
        for label in case["expected"].values()
        for paths in label["required"].values()
        for path in paths
        for ref in path
    }
    return {"hit_at_5": bool(required_sections & top_five), "decisions": decisions}


def evaluate_cases(cases, embeddings, index, reranker, client, *, namespace, model) -> dict:
    """Run retrieval and generation once per question and keep each result locally."""
    root = Path("artifacts/runs")
    root.mkdir(parents=True, exist_ok=True)
    output = Path(mkdtemp(prefix="evaluation-", dir=root))
    metadata = {
        "namespace": namespace,
        "model": model,
        "embedding_model": embeddings.model_name,
        "embedding_revision": embeddings.revision,
        "reranker_model": RERANKER_MODEL,
        "reranker_revision": RERANKER_REVISION,
        "evidence_token_budget": EVIDENCE_TOKEN_BUDGET,
        "dataset_sha256": sha256(GOLD_SET.read_bytes()).hexdigest(),
        "split": cases[0]["split"],
        "scenario_context": SCENARIO_CONTEXT,
    }
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")

    results = []
    errors = 0
    for case in cases:
        question = case["question"]
        started = perf_counter()
        record = {"case_id": case["case_id"], "question": question, "matches": [], "answer": None}
        try:
            candidates = retrieve_hybrid(question, embeddings, index, namespace=namespace)
            ranked = rerank_results(question, candidates, reranker)
            record["candidate_count"] = len(ranked)
            record["matches"] = assemble_evidence(ranked, embeddings.tokenizer)
            record["evidence_tokens"] = sum(
                len(embeddings.tokenizer.encode(hit["body"])) for hit in record["matches"]
            )
            answer = generate_answer(
                f"{question}\n\n{SCENARIO_CONTEXT}", record["matches"], client, model=model
            )
            record["answer"] = answer.model_dump()
        except (APIError, PineconeError, ValueError, RuntimeError) as error:
            # SDK exception bodies may contain request details. Keep the failure type in the run.
            record["error"] = type(error).__name__
            errors += 1
        record["seconds"] = round(perf_counter() - started, 3)
        record["scores"] = score_case(case, record["matches"], record["answer"])
        (output / f"{case['case_id']}.json").write_text(json.dumps(record, indent=2) + "\n")
        results.append(record["scores"])
    decisions = [decision for result in results for decision in result["decisions"].values()]
    full_cases = [result["decisions"] for result in results if len(result["decisions"]) == 3]
    summary = {
        **metadata,
        "artifacts": str(output),
        "cases": len(cases),
        "errors": errors,
        "decisions": len(decisions),
        "exact_decisions": sum(decision["exact"] for decision in decisions),
        "three_decision_cases": len(full_cases),
        "exact_three_decision_cases": sum(
            all(decision["exact"] for decision in case.values()) for case in full_cases
        ),
        "hits_at_5": sum(result["hit_at_5"] for result in results),
        "required_claims": sum(decision["claims"] for decision in decisions),
        "claims_at_5_by_section_id": sum(decision["claims_at_5"] for decision in decisions),
        "claims_in_context_by_section_id": sum(
            decision["claims"] - len(decision["missing_context_claims"]) for decision in decisions
        ),
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary
