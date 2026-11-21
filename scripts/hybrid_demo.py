"""Show the recorded keyword-search win; use --live to repeat the searches."""

import argparse
import json
from pathlib import Path

from pinecone import Pinecone
from sentence_transformers import CrossEncoder

from src.config import AppConfig
from src.embedding import EmbeddingModel
from src.retrieval import (
    RERANKER_MODEL,
    RERANKER_REVISION,
    rerank_results,
    retrieve_dense,
    retrieve_hybrid,
)

RECORDING = Path("evaluation/hybrid_recorded.json")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Query Pinecone; no answer API calls.")
    args = parser.parse_args(argv)
    record = json.loads(RECORDING.read_text())
    if args.live:
        config = AppConfig.from_env()
        config.validate(require_index=True, require_llm=False)
        embeddings = EmbeddingModel(
            config.embedding_model, revision=config.embedding_revision, cache_dir=config.cache_dir
        )
        reranker = CrossEncoder(
            RERANKER_MODEL, revision=RERANKER_REVISION,
            cache_folder=config.cache_dir, device="cpu",
        )
        with Pinecone(api_key=config.pinecone_api_key) as pc:
            description = pc.describe_index(config.pinecone_index_name).to_dict()
            with pc.Index(host=description["host"]) as index:
                for name, retrieve in (("dense", retrieve_dense), ("hybrid", retrieve_hybrid)):
                    hits = retrieve(
                        record["question"], embeddings, index,
                        namespace=record["namespace"], top_k=record["top_k"],
                    )
                    record[name] = rerank_results(record["question"], hits, reranker)[:5]
    print("LIVE SEARCH RESULTS" if args.live else "RECORDED LIVE SEARCH RESULTS")
    print("Question:", record["question"])
    print("Target:", record["expected_section"])
    print("k=5 per search; same reranker; showing children before parent expansion.")
    found = {}
    for name in ("dense", "hybrid"):
        print(f"\n{name.upper()}")
        found[name] = False
        for rank, hit in enumerate(record[name], 1):
            refs = [f"{hit['document_id']}#{section}" for section in hit["section_ids"]]
            marker = " <-- target" if record["expected_section"] in refs else ""
            found[name] |= bool(marker)
            print(f"  {rank}. {', '.join(refs)}{marker}")
    print(f"\nTarget found: vector-only={found['dense']}, hybrid={found['hybrid']}")
    print("This compares direct child retrieval; parent expansion can recover additional clauses.")


if __name__ == "__main__":
    main()
