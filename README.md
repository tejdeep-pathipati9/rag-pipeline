# Flight Disruption Assistant

A retrieval-augmented generation (RAG) project for missed-connection questions about rebooking, overnight accommodation, and refunds. It uses synthetic data for the fictional airline Northstar Air and does not make bookings or process payments.

## Status

The corpus, specifications, and project/dependency setup are merged. The previous uncommitted implementation has been cleared so the pipeline can be rebuilt step by step.

The tokenizer and baseline chunking are implemented locally with tests. Full ingestion, retrieval, and answer generation remain planned. Saved results from the earlier Pinecone demo remain under `artifacts/runs/` as historical evidence.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked --extra dev
cp -n .env.example .env
```

Keep credentials in the local `.env`. The pipeline is being built and reviewed one feature at a time.

## Project data

- `corpus/`: 18 synthetic source documents.
- `specifications/`: independent rules, document manifest, and the unapplied repair overlay.
- `evaluation/`: scenario fixtures and retrieval probes, kept outside the searchable corpus.

The original corpus includes one intentional stale-policy metadata defect for a later controlled debugging exercise.
