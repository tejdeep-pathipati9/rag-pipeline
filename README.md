# Flight Disruption Assistant

A retrieval-augmented generation (RAG) project for missed-connection questions about rebooking, overnight accommodation, and refunds. It uses synthetic data for the fictional airline Northstar Air and does not make bookings or process payments.

## Status

The corpus, specifications, and project setup are merged. Recursive chunking, local MiniLM embeddings, Pinecone ingestion, and hybrid vector/keyword retrieval are implemented. Reranking and answer generation remain planned.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked --extra dev
cp -n .env.example .env
```

Keep credentials in the local `.env`. The pipeline is being built and reviewed one feature at a time.

## Ingestion

Run from the repository root. Set `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` in `.env`. The index must already exist in that API key's project, with stored `body` text and a 384-dimensional `body_vector` field.

Preview chunk counts without writing to Pinecone:

```bash
uv run python -m src --namespace recursive-original-minilm-v1 --dry-run
```

Embed and index the corpus with 200 content tokens and 40-token overlap:

```bash
uv run python -m src --namespace recursive-original-minilm-v1
```

Run the tests:

```bash
uv run pytest -q
```

Each indexed chunk includes its original text, embedding, source metadata, section IDs, and character positions in the Markdown body. Only original text is sent to the embedding model; YAML metadata is stored separately. Text before numbered sections has an empty section list.

Repeating ingestion with unchanged sources and configuration reuses the same chunk IDs. Use a new namespace when changing source content, chunk settings, or the embedding model; ingestion does not delete obsolete chunks from previous configurations.

## Retrieval

Ask a question against the existing indexed namespace:

```bash
uv run python -m src --namespace recursive-original-minilm-v1 --question "Am I eligible for a hotel after a mechanical delay?"
```

This retrieves up to **10 vector matches and 10 keyword matches** from the existing namespace. Vector search uses the configured MiniLM model; keyword search uses Pinecone's existing full-text `body` field with BM25 ranking.

Reciprocal rank fusion combines the lists and removes duplicate chunk IDs, returning up to 20 unique candidates. Results preserve original text and source/citation metadata, with `rrf_score` for the combined order and `vector_score`/`keyword_score` plus ranks when that method found the chunk. This step does not run a learned reranker or generate an answer.

Use the same model, revision, and namespace as ingestion. The original namespace still contains the intentionally stale policy metadata; retrieval preserves it for the later debugging exercise.

## Project data

- `corpus/`: 18 synthetic source documents.
- `specifications/`: independent rules, document manifest, and the unapplied repair overlay.
- `evaluation/`: scenario fixtures and retrieval probes, kept outside the searchable corpus.

The original corpus includes one intentional stale-policy metadata defect for a later controlled debugging exercise.
