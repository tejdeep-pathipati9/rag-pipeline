"""Ingest sources, answer questions, or run the offline-labeled benchmark."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from anthropic import AnthropicFoundry, APIError
from dotenv import load_dotenv
from pinecone import NotFoundError, Pinecone
from sentence_transformers import CrossEncoder
from transformers.utils import logging as transformers_logging

from src.chunking import MarkdownChunker, ParentChildChunker, RecursiveChunker
from src.documents import prepare_chunks
from src.embedding import DEFAULT_MODEL, DEFAULT_REVISION, EmbeddingModel
from src.evaluation import evaluate_cases, select_cases
from src.ingestion import ingest_chunks, validate_index
from src.model import FlightAnswer, generate_answer
from src.retrieval import (
    EVIDENCE_TOKEN_BUDGET,
    RERANKER_MODEL,
    RERANKER_REVISION,
    TOP_K,
    assemble_evidence,
    rerank_results,
    retrieve_hybrid,
)


def _format_answer(answer: FlightAnswer, matches: list[dict], *, details: bool = False) -> str:
    """Keep the summary and citations visible in both terminal views."""
    titles = {hit["document_id"]: hit["title"] for hit in matches if "title" in hit}
    lines = [answer.summary, ""]
    for label, decision in (
        ("Rebooking", answer.rebooking),
        ("Hotel", answer.hotel),
        ("Refund", answer.refund),
    ):
        status = decision.status.replace("_", " ").capitalize()
        heading = f"{label} · {status}"
        sections: dict[str, list[str]] = {}
        for citation in dict.fromkeys(decision.citations):
            doc, _, section = citation.partition("#")
            sections.setdefault(doc, []).append(section)

        if details:
            lines.extend((heading, decision.explanation))
            if decision.missing_facts:
                lines.append("Still needed")
                lines.extend(f"  - {fact}" for fact in decision.missing_facts)
            if sections:
                lines.append("Sources")
                for doc, numbers in sections.items():
                    source = f"{titles[doc]} ({doc})" if doc in titles else doc
                    references = ", ".join(f"§{number}" for number in numbers)
                    lines.append(f"  - {source}, {references}")
            lines.append("")
        else:
            references = "; ".join(
                f"{doc} {', '.join(f'§{number}' for number in numbers)}"
                for doc, numbers in sections.items()
            )
            lines.append(f"{heading}  [{references}]" if references else heading)
    return "\n".join(lines).rstrip()


def main(argv=None):
    """Ingest sources, retrieve/rerank evidence, and optionally generate an answer."""
    parser = argparse.ArgumentParser(
        description="Ingest sources or retrieve and rerank ten vector and ten keyword candidates."
    )
    parser.add_argument(
        "--namespace", required=True, help="Namespace for one fixed corpus/model/config."
    )
    parser.add_argument("--chunk-size", type=int, default=200)
    parser.add_argument("--overlap", type=int, default=40)
    parser.add_argument(
        "--chunk-strategy",
        choices=("recursive", "markdown", "parent-child"),
        help="Choose how to split Markdown during ingestion or a dry run.",
    )
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument(
        "--question", help="Retrieve existing chunks and rerank them with a local cross-encoder."
    )
    parser.add_argument(
        "--generate", action="store_true", help="Generate a cited answer using Azure Foundry."
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--details", action="store_true", help="Show full answer explanations.")
    output.add_argument(
        "--json", action="store_true", help="Include full retrieval details for a generated answer."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Inspect chunks without writing to Pinecone."
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run the benchmark using Pinecone and Azure Foundry.",
    )
    parser.add_argument("--split", choices=("development", "test"), help="Evaluation split.")
    parser.add_argument(
        "--case-id", action="append", help="Limit evaluation to a case in the split."
    )
    args = parser.parse_args(argv)
    if args.chunk_strategy and (args.question is not None or args.evaluate):
        parser.error("--chunk-strategy applies to ingestion; the namespace selects indexed chunks.")
    cases = []
    if args.evaluate:
        if args.question is not None or args.generate or args.dry_run:
            parser.error("--evaluate runs its own questions with generation enabled.")
        try:
            cases = select_cases(args.split or "development", args.case_id or [])
        except (OSError, ValueError) as error:
            parser.error(f"Cannot select evaluation cases: {error}")
    elif args.split or args.case_id:
        parser.error("--split and --case-id require --evaluate.")
    if args.generate and args.question is None:
        parser.error("--generate requires --question.")
    if args.details and not args.generate:
        parser.error("--details requires --generate.")
    if args.question is not None:
        if not args.question.strip():
            parser.error("--question must not be empty.")
        if args.dry_run:
            parser.error("--dry-run is for ingestion; omit it when using --question.")
    load_dotenv(".env")
    llm_api_key = os.getenv("LLM_API_KEY", "")
    llm_model = os.getenv("LLM_MODEL", "")
    llm_base_url = os.getenv("LLM_BASE_URL", "")
    if (args.generate or args.evaluate) and not all((llm_api_key, llm_model, llm_base_url)):
        parser.error("Set LLM_API_KEY, LLM_MODEL and LLM_BASE_URL in your local .env.")

    if args.generate and not (args.details or args.json):
        transformers_logging.disable_progress_bar()
    embeddings = EmbeddingModel(
        os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL),
        revision=os.getenv("EMBEDDING_REVISION", DEFAULT_REVISION),
        cache_dir=os.getenv("MODEL_CACHE_DIR", ".cache/models"),
    )
    summary: dict = {
        "namespace": args.namespace,
        "embedding_model": embeddings.model_name,
        "embedding_revision": embeddings.revision,
        "dimension": embeddings.dimension,
    }
    chunks: list[dict] = []
    if args.question is None and not args.evaluate:
        if args.chunk_size > embeddings.max_content_tokens:
            parser.error(
                f"--chunk-size must be at most {embeddings.max_content_tokens} content tokens."
            )
        chunker_class = {
            "recursive": RecursiveChunker,
            "markdown": MarkdownChunker,
            "parent-child": ParentChildChunker,
        }[args.chunk_strategy or "recursive"]
        chunker = chunker_class(embeddings.tokenizer, args.chunk_size, args.overlap)
        # Retrieval skips preparation entirely: it searches already-indexed chunks.
        chunks = prepare_chunks(Path("corpus"), chunker)
        summary.update(
            {
                "chunk_size": args.chunk_size,
                "overlap": args.overlap,
                "chunk_strategy": chunker.strategy,
                "documents": len({chunk["document_id"] for chunk in chunks}),
                "chunks": len(chunks),
                "chunks_per_document": dict(Counter(chunk["document_id"] for chunk in chunks)),
                "upserted": 0,
                "dry_run": args.dry_run,
            }
        )
        if args.dry_run:
            print(json.dumps(summary, indent=2))
            return

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if not api_key or not index_name:
        parser.error("Set PINECONE_API_KEY and PINECONE_INDEX_NAME in your local .env.")
    with Pinecone(api_key=api_key) as client:
        try:
            description = client.describe_index(index_name).to_dict()
        except NotFoundError:
            parser.error(
                f"Pinecone index {index_name!r} was not found in this API key's project. "
                "Check PINECONE_INDEX_NAME and PINECONE_API_KEY, or create the index first."
            )
        validate_index(description, embeddings.dimension)
        with client.Index(host=description["host"]) as index:
            if args.evaluate:
                reranker = CrossEncoder(
                    RERANKER_MODEL,
                    revision=RERANKER_REVISION,
                    cache_folder=os.getenv("MODEL_CACHE_DIR", ".cache/models"),
                    device="cpu",
                )
                with AnthropicFoundry(
                    api_key=llm_api_key, base_url=llm_base_url, timeout=60.0
                ) as llm:
                    evaluation = evaluate_cases(
                        cases,
                        embeddings,
                        index,
                        reranker,
                        llm,
                        namespace=args.namespace,
                        model=llm_model,
                    )
                summary["evaluation"] = evaluation
            elif args.question is not None:
                summary.update(
                    {
                        "question": args.question,
                        "top_k_per_method": TOP_K,
                        "retrieval_method": "hybrid",
                        "matches": retrieve_hybrid(
                            args.question, embeddings, index, namespace=args.namespace
                        ),
                    }
                )
            else:
                summary["upserted"] = ingest_chunks(
                    chunks,
                    embeddings,
                    index,
                    namespace=args.namespace,
                    batch_size=args.batch_size,
                )
    summary["index"] = index_name

    if args.question is not None:
        summary["reranker_model"] = RERANKER_MODEL
        summary["reranker_revision"] = RERANKER_REVISION
        # Skip loading another model when retrieval found no evidence.
        if summary["matches"]:
            reranker = CrossEncoder(
                RERANKER_MODEL,
                revision=RERANKER_REVISION,
                cache_folder=os.getenv("MODEL_CACHE_DIR", ".cache/models"),
                device="cpu",
            )
            summary["matches"] = rerank_results(args.question, summary["matches"], reranker)
        summary["candidate_count"] = len(summary["matches"])
        summary["matches"] = assemble_evidence(summary["matches"], embeddings.tokenizer)
        summary["evidence_token_budget"] = EVIDENCE_TOKEN_BUDGET
        summary["evidence_tokens"] = sum(
            len(embeddings.tokenizer.encode(hit["body"])) for hit in summary["matches"]
        )

    # Generation is opt-in: the existing retrieval command does not call a paid LLM.
    if args.generate and args.question is not None:
        with AnthropicFoundry(api_key=llm_api_key, base_url=llm_base_url, timeout=60.0) as llm:
            try:
                answer = generate_answer(args.question, summary["matches"], llm, model=llm_model)
            except (APIError, ValueError, RuntimeError) as error:
                parser.error(f"Generation failed: {error}")
        if not args.json:
            print(_format_answer(answer, summary["matches"], details=args.details))
            return
        summary["generation_model"] = llm_model
        summary["answer"] = answer.model_dump()

    print(json.dumps(summary, indent=2))
    if args.evaluate and summary["evaluation"]["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
