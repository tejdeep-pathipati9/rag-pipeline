# Northstar Policy Q&A

A retrieval-augmented assistant for a fictional airline's rebooking, hotel, meal and refund policies. Answers include policy titles, document IDs, section citations and any missing information.

Five Markdown policies (644–789 words each) are searched with MiniLM embeddings and Pinecone vector/BM25 retrieval. Reciprocal rank fusion combines candidates, a local cross-encoder reranks them, and Azure Foundry generates an answer from the selected evidence. Parent-child chunking uses 200-token children, 40-token recursive-fallback overlap and a 4,000-source-token evidence budget. The child limit fits MiniLM's 254-content-token window; fallback overlap retains context across long blocks.

## Setup

Requires Python 3.11+, `uv`, a Pinecone document index and an Azure Foundry deployment.

```bash
uv sync --locked --extra dev
cp -n .env.example .env
```

Set `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `LLM_API_KEY`, `LLM_BASE_URL` and `LLM_MODEL` in `.env`. The index needs stored `body` text and a 384-dimensional `body_vector` field. Keep credentials local.

## Ask questions

```bash
uv run python -m src --dry-run   # Preview source chunks
uv run python -m src --ingest    # Index the policies
uv run python -m src             # Interactive questions; type exit to finish
```

Example: “I'm stuck overnight because of bad weather. Will Northstar pay for my hotel?”

The default namespace is `policy-qa-compact-parent-child-v1`. Use `--namespace NAME` to select another index namespace. Ingestion supports `--chunk-strategy recursive`, `markdown` or `parent-child`. Use a separate namespace when changing source content or chunking settings.

## Evaluation

The benchmark contains 15 fixed natural-language questions. Hybrid retrieval requests 20 candidates per search method before reranking and evidence assembly.

```bash
uv run python -m scripts.evaluate                     # Live retrieval and answers
uv run python -m scripts.evaluate --retrieval-only    # Skip answer generation
uv run python -m scripts.evaluate --search dense      # Vector-only comparison
uv run pytest -q                                     # Offline tests and recorded-answer checks
```

Live hybrid results on November 20, 2026, with the same questions, models and evidence budget:

| Chunking | Recall@5 | Recall@10 | Final-context section recall |
|---|---:|---:|---:|
| Recursive | 78.9% | 88.9% | 100% |
| Markdown | 78.9% | 87.8% | 100% |
| Parent-child | 78.9% | **91.1%** | 100% |

Recall@5 and recall@10 measure ranked chunks before parent expansion. The parent-child live run passed 15/15 expected-phrase/citation checks with no service errors. These checks are not semantic accuracy or citation-entailment scores. The [recorded comparison](evaluation/chunking_comparison.json) and [actual answers with evidence](evaluation/policy_qa_recorded.json) are included for inspection.

The evaluator writes `artifacts/evaluation.md` and `artifacts/evaluation.json` locally. CI runs Ruff and pytest without service credentials or API calls.

## Demonstrations

```bash
uv run python -m scripts.minimal_demo         # Live two-passage embed/store/retrieve
uv run python -m scripts.hybrid_demo          # Recorded live keyword-search comparison
uv run python -m scripts.hybrid_demo --live   # Repeat the Pinecone searches
uv run python -m scripts.source_failure_demo # Recorded live source failure and repair
```

The hybrid query asks about `NO_CURRENT_INVENTORY`. Vector-only misses the specific clause in its top five children; BM25 retrieves it and hybrid reranking places it first. Parent expansion recovers the clause for both, so this demonstrates a direct child-retrieval improvement.

The source-quality demonstration republishes the old crew-hotel exclusion in an isolated current-labelled policy export. Retrieval supplies the relevant clauses, but the stale text produces a wrong denial. Repairing only the source changes the response to the correct standard benefit; fresh retrieval confirms the repair. The question, prompt and model stay fixed. This is separate from the historical policy's incorrect status flag, which did not cause the earlier probes to fail.

Export the exact broken and corrected demonstration sources for inspection:

```bash
uv run python -m scripts.source_failure_demo --export-dir artifacts/runs/source-quality
```

The policies are synthetic and do not establish real airline or legal entitlements. Evaluation questions, expected answers and generated outputs are excluded from the searchable corpus.
