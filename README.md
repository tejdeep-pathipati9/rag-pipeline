# Flight Disruption Assistant

A retrieval-augmented generation (RAG) project for missed-connection questions about rebooking, overnight accommodation, and refunds. It uses synthetic data for the fictional airline Northstar Air and does not make bookings or process payments.

## Status

The corpus, specifications, and project setup are merged. Recursive chunking, local MiniLM embeddings, Pinecone ingestion, hybrid retrieval, cross-encoder reranking, and Azure Foundry answer generation are implemented.

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

Reciprocal rank fusion combines the lists and removes duplicate chunk IDs. A local `cross-encoder/ms-marco-MiniLM-L6-v2` then scores each question–chunk text pair and sorts all candidates by relevance. The first run downloads the pinned reranker into the model cache; no extra dependency or API key is needed.

Results keep up to 20 unique chunks, preserving original text and source/citation metadata. Each has a `rerank_score`, the earlier `rrf_score`, and `vector_score`/`keyword_score` plus ranks when that method found the chunk. Equal reranker scores retain the fused order. Scores indicate relevance, not eligibility or confidence; reranking cannot recover evidence missed by both searches. Use `--generate` to turn the reranked evidence into an answer.

Use the same model, revision, and namespace as ingestion. The original namespace still contains the intentionally stale policy metadata; retrieval preserves it for the later debugging exercise.

## Answer generation

Configure your Azure Foundry deployment in the local `.env`:

- `LLM_API_KEY`: the Foundry resource key.
- `LLM_BASE_URL`: the Claude Messages endpoint, such as `https://your-resource.services.ai.azure.com/anthropic`.
- `LLM_MODEL`: your exact deployment name for the Opus model.

Generate an answer from the reranked hybrid retrieval results:

```bash
uv run python -m src --namespace recursive-original-minilm-v1 --question "For FR-214 on 2026-10-14, what are my rebooking, hotel, and refund options?" --generate
```

The output includes a summary and separate rebooking, hotel, and refund decisions, each with an explanation, citations, and missing facts. Citations use `DOCUMENT_ID#SECTION_ID` and are checked against the retrieved chunks. Missing evidence produces `NEEDS_REVIEW`; response validation checks structure and citation references, not the factual correctness of every explanation.

Generation uses the configured Azure API and is opt-in. Omitting `--generate` runs retrieval only. API keys, independent rule specifications, and evaluation labels are never included in the generation prompt.

## Project data

- `corpus/`: 18 synthetic source documents.
- `specifications/`: independent rules, document manifest, and the unapplied repair overlay.
- `evaluation/`: scenario fixtures and retrieval probes, kept outside the searchable corpus.

The original corpus includes one intentional stale-policy metadata defect for a later controlled debugging exercise.
