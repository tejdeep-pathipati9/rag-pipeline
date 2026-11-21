"""Ask policy questions interactively or ingest sources."""

import argparse
import json
from collections import Counter
from pathlib import Path

from anthropic import AnthropicFoundry
from pinecone import NotFoundError, Pinecone
from sentence_transformers import CrossEncoder
from transformers.utils import logging as transformers_logging

from src.config import CHUNKING_STRATEGIES, AppConfig, ChunkingConfig
from src.documents import prepare_chunks
from src.embedding import EmbeddingModel
from src.ingestion import ingest_chunks, validate_index
from src.retrieval import RERANKER_MODEL, RERANKER_REVISION
from src.terminal import interactive_session


def main(argv=None):
    """Open the question prompt, index policies, or preview chunks."""
    config = AppConfig.from_env()
    chunking = ChunkingConfig()
    parser = argparse.ArgumentParser(
        description="Ask Northstar policy questions interactively (default), or index policies."
    )
    parser.add_argument(
        "--namespace", default=config.namespace,
        help="Indexed namespace (default: %(default)s)."
    )
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--ingest", action="store_true", help="Embed and index the corpus.")
    operation.add_argument(
        "--dry-run", action="store_true", help="Inspect chunks without writing to Pinecone."
    )
    parser.add_argument("--chunk-size", type=int, default=chunking.chunk_size)
    parser.add_argument("--overlap", type=int, default=chunking.overlap)
    parser.add_argument(
        "--chunk-strategy",
        choices=tuple(CHUNKING_STRATEGIES),
        help="Choose how to split Markdown during ingestion or a dry run.",
    )
    parser.add_argument("--batch-size", type=int, default=config.batch_size)
    args = parser.parse_args(argv)
    interactive = not (args.ingest or args.dry_run)
    if args.chunk_strategy and interactive:
        parser.error("--chunk-strategy applies to ingestion; the namespace selects indexed chunks.")
    try:
        config.validate(require_index=not args.dry_run, require_llm=interactive)
    except ValueError as error:
        parser.error(str(error))

    if interactive:
        transformers_logging.disable_progress_bar()
        print("Loading Northstar Policy Q&A...", flush=True)
    embeddings = EmbeddingModel(
        config.embedding_model,
        revision=config.embedding_revision,
        cache_dir=config.cache_dir,
    )
    summary: dict = {
        "namespace": args.namespace,
        "embedding_model": embeddings.model_name,
        "embedding_revision": embeddings.revision,
        "dimension": embeddings.dimension,
    }
    chunks: list[dict] = []
    if args.ingest or args.dry_run:
        if args.chunk_size > embeddings.max_content_tokens:
            parser.error(
                f"--chunk-size must be at most {embeddings.max_content_tokens} content tokens."
            )
        chunking = ChunkingConfig(
            strategy=args.chunk_strategy or chunking.strategy,
            chunk_size=args.chunk_size,
            overlap=args.overlap,
        )
        try:
            chunker = chunking.create_chunker(embeddings.tokenizer)
        except ValueError as error:
            parser.error(str(error))
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

    with Pinecone(api_key=config.pinecone_api_key) as client:
        try:
            description = client.describe_index(config.pinecone_index_name).to_dict()
        except NotFoundError:
            parser.error(
                f"Pinecone index {config.pinecone_index_name!r} was not found "
                "in this API key's project. "
                "Check PINECONE_INDEX_NAME and PINECONE_API_KEY, or create the index first."
            )
        validate_index(description, embeddings.dimension)
        with client.Index(host=description["host"]) as index:
            if interactive:
                reranker = CrossEncoder(
                    RERANKER_MODEL,
                    revision=RERANKER_REVISION,
                    cache_folder=config.cache_dir,
                    device="cpu",
                )
                with AnthropicFoundry(
                    api_key=config.llm_api_key, base_url=config.llm_base_url, timeout=120.0
                ) as llm:
                    interactive_session(
                        embeddings, index, reranker, llm,
                        namespace=args.namespace, model=config.llm_model,
                        top_k=config.retrieval_k,
                    )
                    return
            else:
                summary["upserted"] = ingest_chunks(
                    chunks,
                    embeddings,
                    index,
                    namespace=args.namespace,
                    batch_size=args.batch_size,
                )
    summary["index"] = config.pinecone_index_name

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
