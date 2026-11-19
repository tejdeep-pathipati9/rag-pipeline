# Flight Disruption Assistant

**18 `.md` source documents**, an independent fictional-airline rule specification, a broken-source repair overlay, and **40 labeled synthetic evaluation cases**.

**Expanded corpus:** Core policy documents are now approximately 1,400–1,700 words, with detailed eligibility rules, evidence requirements, and interdependent subsections. SOPs are over 1,000 words and historical case reports are about 800–900 words. Structured operational records remain intentionally concise. See `evaluation/document_word_counts.md` for exact counts. The original section IDs, 40 gold cases, and single planted stale-source-status defect have been preserved.

The repository now includes the **Phase 0–1 Python CLI** for corpus validation and a real two-passage Pinecone smoke test. Full-corpus ingestion, retrieval experiments, and answer generation are not implemented yet. It is designed for a Pinecone-based RAG lab on missed domestic flight connections. The fictional carrier **Northstar Air** does not exist. Ticket, passenger, incident, flight and voucher examples are synthetic; no booking or flight inventory is live.

## Run the Phase 0–1 implementation

Use Python 3.11+ and [uv](https://docs.astral.sh/uv/). From the repository root, a fresh setup is:

```bash
# Lightweight validation and offline tests; does not install the local ML model stack.
uv sync --locked --extra dev
uv run --no-sync python -m src validate-corpus
uv run --no-sync pytest -q
uv run --no-sync ruff check src tests

# Add the local model stack for the hosted two-passage experiment.
uv sync --locked --extra dev --extra smoke
cp -n .env.example .env
```

Edit `.env` locally to set `PINECONE_API_KEY` and `PINECONE_INDEX_NAME`. Keep the dedicated `smoke-` namespace. Preserve any existing `.env` instead of copying over it. Environment variables take precedence over `.env` values.

```bash
# First run: explicitly permit creating the configured index if absent.
uv run --no-sync python -m src smoke-pinecone --create-index

# Subsequent runs: use the existing index and upsert the same two stable IDs.
uv run --no-sync python -m src smoke-pinecone
```

The smoke command uses local, revision-pinned MiniLM embeddings (384 dimensions), a Pinecone document index with a cosine `body_vector` field and full-text `body` field, and exactly two demonstration texts. It never ingests corpus/evaluation/specification files. Index creation defaults to AWS `us-east-1`, configurable in `.env`. Existing incompatible schemas fail before writes.

Each smoke run saves `config.json`, `result.json`, and `terminal.txt` in a new `artifacts/runs/smoke-<run-id>/` directory. A pass requires both newly written texts to be fetchable and searchable and the relevant passage to score strictly higher. Missing configuration is recorded as `not_run`; provider or ranking failures are recorded as `failed`. Artifacts and model caches are gitignored. These terminal transcripts are real command/result evidence; screenshot capture for the submission PDF is still outstanding.

For the existing development environment, activate `.venv` and use `python -m src ...` directly. A pip installation alternative is `python -m pip install -e '.[dev,smoke]'`; exact transitive versions are provided by `uv.lock` when using uv.

Offline tests prohibit network connections. The hosted pytest test is opt-in and requires an existing compatible index:

```bash
FLIGHT_DISRUPTION_LIVE_TEST=1 uv run --no-sync pytest -q -m integration
```

No CI run or full RAG benchmark is claimed at this stage. Run evidence is saved under `artifacts/runs/`; the plan defines the review gate before Phase 2.

## Directory contents

- `corpus/policies/` — five Northstar policies, including a historical 2025 edition.
- `corpus/regulatory/` — two attributed Markdown research digests summarizing actual DOT sources; these are not fictional Northstar policy and should not be mistaken for controlling legal text.
- `corpus/procedures/` — three procedural SOPs for rebooking, hotel and refunds.
- `corpus/records/` — four connected booking, flight, cause, and offer records for case `FR-214`.
- `corpus/cases/` — four independent historical cases with differing outcomes.
- `specifications/authoritative_rules.yaml` — **do not index**; defines independently maintained synthetic ground truth.
- `specifications/corpus_manifest.yaml` — document IDs, hashes, types, dates and source paths.
- `specifications/data_quality_repair.yaml` — correction for the purposely stale current-status flag. **Do not apply before the required debugging demonstration.**
- `evaluation/golden_cases.jsonl` — 40 independently held-out scenario fixtures; do not index. These are rule-derived provisional gold labels and should be reviewed before reporting evaluation metrics.

## Intentionally planted data-quality defect

`corpus/policies/05_passenger_care_2025.md` has `status: current` in frontmatter. This **incorrect** metadata is the single planted source defect. The text is a preserved historical 2025 edition; its crew-delay exclusion differs from the 2026 policy. At 2026 travel dates, it should be archived (`superseded`) with an end date of 2025-12-31. Record the flawed output and retrieved sources before applying `data_quality_repair.yaml`. Evaluate version filters and freshness separately from relevance ranking.

**Important:** Metadata alone cannot guarantee that a bad answer occurs; the lab must show an actual flawed answer and reproduce whether it came from the bad source field. If retrieval selects the 2026 rule despite the defect, do not claim that the defect caused a failed answer. Inspect eligibility filters, rankings and retrieved evidence to reproduce a meaningful failure.

## Retrieval experiments (do not force a single strategy on every file)

1. Recursive baseline: token-bounded sentence/paragraph chunks with documented overlap.
2. Structure-aware: preserve policy headings, sections, tables and footnotes.
3. Structure-aware with parent-child: index clause-level child embeddings; use stable `parent_id` to fetch complete logical sections, notably NS-CARE-2026 §4 and SOP-HOTEL §2.
4. Contextual clause-aware: embed each provision with section path, policy identity and resolved reference identifiers; preserve original wording and retrieve linked clauses, notably NS-REF-2026 §3.
5. Mixed production-style: use record-level exact lookup for source-of-truth structured records and semantic search for prose.

Run all selected variants against the same underlying sources, candidate budget and fixed test questions. For parent expansion, additionally compare at a consistent total evidence-token budget. Capture retrieval recall, evidence completeness, case-level resolution accuracy, citation correctness, latency and index size.

## Lab implementation checklist

- Demonstrate a **two-text** embedding → Pinecone upsert → query before full ingestion.
- Write at least one query where dense-only misses an exact section ID and dense+keyword hybrid retrieval succeeds.
- Implement candidate reranking (cross-encoder or equivalent) after candidate retrieval; preserve the original ranking in traces.
- Keep `golden_cases.jsonl` out of the Pinecone source index, evaluate with `pytest` and freeze expected answers before experiments.
- Source every decision to actual source sections, not only similar historical outcomes.
- Run a controlled **broken-source** experiment and then verify repair/reindexing; capture both terminal outputs.
- Run automated tests in CI; screenshots/PDF deliverable are separate and not included in this source package.

## Regulatory sources and scope

Reference digests paraphrase official DOT materials viewed 2026-11-18:
- https://www.transportation.gov/individuals/aviation-consumer-protection/refunds
- https://www.transportation.gov/airconsumer/airline-customer-service-dashboard
- https://www.transportation.gov/airconsumer/airline-cancellation-delay-dashboard

The DOT dashboard covers **listed real airline commitments**, not Northstar; it must not be used to assign benefits to a fictional carrier. The DOT refund page was listed as updated 2025-11-07 when checked. Reverify legal/regulatory details for real-world deployment.
