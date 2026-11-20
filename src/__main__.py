"""Ingest sources, or search vectors and keywords by adding --question TEXT."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from pinecone import NotFoundError, Pinecone

from src.chunking import RecursiveChunker
from src.documents import prepare_chunks
from src.embedding import DEFAULT_MODEL, DEFAULT_REVISION, EmbeddingModel
from src.ingestion import ingest_chunks, validate_index
from src.retrieval import TOP_K, retrieve_hybrid


def main(argv=None):
    """Use the same model and index for corpus ingestion and question retrieval."""
    parser = argparse.ArgumentParser(
        description="Ingest sources or retrieve ten vector and ten keyword candidates."
    )
    parser.add_argument(
        "--namespace", required=True, help="Namespace for one fixed corpus/model/config."
    )
    parser.add_argument("--chunk-size", type=int, default=200)
    parser.add_argument("--overlap", type=int, default=40)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument(
        "--question", help="Search existing chunks using vector and keyword retrieval."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Inspect chunks without writing to Pinecone."
    )
    args = parser.parse_args(argv)
    if args.question is not None:
        if not args.question.strip():
            parser.error("--question must not be empty.")
        if args.dry_run:
            parser.error("--dry-run is for ingestion; omit it when using --question.")
    load_dotenv(".env")

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
    if args.question is None:
        if args.chunk_size > embeddings.max_content_tokens:
            parser.error(
                f"--chunk-size must be at most {embeddings.max_content_tokens} content tokens."
            )
        chunker = RecursiveChunker(embeddings.tokenizer, args.chunk_size, args.overlap)
        # Retrieval skips preparation entirely: it searches already-indexed chunks.
        chunks = prepare_chunks(Path("corpus"), chunker)
        summary.update(
            {
                "chunk_size": args.chunk_size,
                "overlap": args.overlap,
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
            if args.question is not None:
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

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
