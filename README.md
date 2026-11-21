# Northstar Policy Q&A

A small RAG assistant that answers questions about fictional Northstar Air policies
with document and section citations. It explains published rules; it does not look
up passengers, book flights, issue hotel vouchers or process refunds.

## Documents

The corpus contains five policy documents in `corpus/policies/`:

- `NS-CONN-2026`: protected connections and rebooking.
- `NS-CARE-2026`: hotel and passenger-care commitments.
- `NS-REF-2026`: refunds and passenger choice.
- `NS-CAUSE-2026`: disruption classifications and approved findings.
- `NS-CARE-2025`: the outdated care policy, deliberately mislabeled `current`.

Ingestion includes only the corpus documents. Evaluation questions and reference
specifications are kept outside the retrieval index.

## Setup

Requires Python 3.11+ and uv:

```bash
uv sync --locked --extra dev
cp -n .env.example .env
```

Set `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` locally. The existing index needs a
stored, searchable `body` string field and a 384-dimensional `body_vector` field.
For generation, set `LLM_API_KEY`, `LLM_BASE_URL` and `LLM_MODEL` for Azure Foundry.
Credentials are never stored in source files or evaluation artifacts.
`AppConfig` in `src/config.py` loads these settings and holds the default namespace,
batch size and model cache location for both the CLI and evaluation script.

## Index the policies

Use a separate namespace for each corpus and chunking configuration.

```bash
uv run python -m src --dry-run
uv run python -m src --ingest
```

Chunking defaults are set in `ChunkingConfig` in `src/config.py`: strategy
`parent-child`, chunk size `200`, and overlap `40`. CLI flags override these for a run.
Changes apply when indexing; querying uses the chunks already in the chosen namespace.

The default embeds children of at most 200 content tokens, below MiniLM's
254-content-token limit. Children follow Markdown headings and blocks; oversized
blocks use recursive splitting with 40-token overlap. Retrieval expands selected
children to complete level-two source sections and deduplicates parents, keeping
related clauses and tables together. Evidence is capped at 4,000 source-content
tokens. Text, source offsets, policy versions, section IDs and stable chunk IDs
are preserved. Repeating the same configuration overwrites the same IDs; changed
documents need a new namespace.

`--chunk-strategy recursive` and `--chunk-strategy markdown` support comparisons
when indexing into separate namespaces.

## Ask questions

Start the interactive prompt:

```bash
uv run python -m src
```

Type a question and press Enter. Each answer includes policy citations and any
missing information. Keep asking questions without reloading the models; type
`/help` for examples or `exit` to leave. Each question is answered independently
and uses your configured Pinecone and Azure Foundry services.

The default namespace is `policy-qa-parent-child-200-40-v1`; use `--namespace` to
choose another, including the `policy-qa-recursive-v1` baseline.

Questions without a date use the current policy as of today in America/New_York.
Explicit dates and relative dates such as "last year" are respected. Evaluation
freezes its reference date so historical questions remain reproducible.

`AppConfig.retrieval_k` sets how many candidates each search method retrieves.
The default is 20 per method; the evidence budget stays at 4,000 content tokens.
Retrieval combines dense matches with Pinecone BM25 matches using reciprocal
rank fusion. A pinned MiniLM cross-encoder reranks the unique candidates. Scores
measure relevance, not policy applicability or confidence. Dates and policy versions
must still be checked, especially while the planted metadata defect is present.

## Evaluate

```bash
uv run python -m scripts.evaluate
uv run python -m scripts.evaluate --retrieval-only --top-k 20
uv run pytest -q
```

The active benchmark has 15 fixed policy questions in
`evaluation/flight_disruption_gold_set.jsonl`. Evaluation prints retrieval recall
and answer-check accuracy. Open `artifacts/evaluation.md` for a per-question table,
missing sections, and expandable answers. Full retrieved text remains in
`artifacts/evaluation.json` for debugging. Each run replaces those two files.

`--top-k` changes the candidate count per search method. Ranked chunk recall@5 and
recall@10 are measured before parent expansion; first-five context-entry recall is reported
separately because parent sections are larger. `--retrieval-only` skips Azure calls and reports
answer accuracy as not measured. Candidate-pool and final-context recall help show
whether missing evidence was never retrieved or was lost during selection.

Retrieval recall is the fraction of listed gold section IDs found in the ranked
chunks or assembled context. Section overlap does not guarantee that a full clause was
provided. Answer accuracy requires all expected phrase groups and a supporting
citation path, including listed equivalent clauses. These are key-information checks, not a full
semantic or citation-entailment judge; inspect the saved text for unsupported claims.
The offline tests cover 15 independent reference answers, real source mappings,
citation validation, SDK serialization, retrieval plumbing and evaluation math.
