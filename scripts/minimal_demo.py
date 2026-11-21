"""Prove embed-store-retrieve with two known passages in an isolated namespace."""

import time

from pinecone import Pinecone

from src.config import AppConfig
from src.embedding import EmbeddingModel
from src.ingestion import validate_index
from src.retrieval import retrieve_dense

NAMESPACE = "demo-two-passages-v1"
PASSAGES = {
    "hotel-policy": "Northstar hotel reimbursement requires written authorization before booking.",
    "gardening": "Tomato plants need sunlight, regular watering and well-drained garden soil.",
}
QUESTION = "Do I need approval before booking my own hotel?"


def main():
    config = AppConfig.from_env()
    config.validate(require_index=True, require_llm=False)
    embeddings = EmbeddingModel(
        config.embedding_model, revision=config.embedding_revision, cache_dir=config.cache_dir
    )
    with Pinecone(api_key=config.pinecone_api_key) as pc:
        description = pc.describe_index(config.pinecone_index_name).to_dict()
        validate_index(description, embeddings.dimension)
        with pc.Index(host=description["host"]) as index:
            for identity, text in PASSAGES.items():
                vector = embeddings.embed_documents([text])[0]
                result = index.documents.upsert(
                    namespace=NAMESPACE,
                    documents=[{"_id": identity, "body": text, "body_vector": vector}],
                )
                assert result.upserted_count == 1
                print(f"Stored {identity}: {len(vector)}-dimensional embedding", flush=True)
            # Acknowledged writes can take a few seconds to become searchable.
            deadline = time.monotonic() + 30
            while True:
                hits = retrieve_dense(
                    QUESTION, embeddings, index, namespace=NAMESPACE, top_k=2
                )
                if len(hits) == 2:
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError("Both passages are not yet visible in Pinecone.")
                time.sleep(1)
    print(f"\nQuestion: {QUESTION}")
    for rank, hit in enumerate(hits, 1):
        print(f"{rank}. {hit['_id']} ({hit['_score']:.4f}): {hit['body']}")
    assert hits[0]["_id"] == "hotel-policy"
    print("PASS: the relevant hotel passage ranks above the unrelated gardening passage.")


if __name__ == "__main__":
    main()
