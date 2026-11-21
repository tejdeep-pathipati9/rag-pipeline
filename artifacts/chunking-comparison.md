# Chunking comparison

Same 15 development questions and unchanged golden set; 200-token children, 40-token fallback overlap, k=20 per search, the same MiniLM models, and a 4,000-token evidence budget. New strategy namespaces leave the recursive baseline intact.

| Strategy | Indexed chunks | Chunk recall@5 | Chunk recall@10 | First-five context recall | Final context recall | Complete-section coverage |
|---|---:|---:|---:|---:|---:|---:|
| recursive | 100 | 54.4% | 67.8% | 54.4% | 96.7% | 83.3% |
| markdown | 77 | 61.1% | 74.4% | 61.1% | 87.8% | 87.8% |
| parent-child | 83 | 64.4% | 71.1% | 91.1% | 94.4% | 94.4% |

## What the numbers mean

- Ranked chunk recall@5 and recall@10 are measured on the retrieved children before parent expansion. This is the ranking comparison.
- Parent-child expands children into complete level-two sections. Its 91.1% first-five context recall uses larger units and must not be presented as a 91.1% chunk-ranking score.
- Complete-section coverage requires the entire listed gold section text to be present in the assembled spans, ignoring whitespace-only gaps. It is stricter than merely finding an overlapping section ID, but does not grade semantics.
- Parent-child has the strongest recall@5 and complete-section coverage. Markdown leads recall@10 (74.4% vs parent-child 71.1%), so neither wins at every cutoff. Parent-child final section-ID recall is slightly lower than recursive (94.4% vs 96.7%).

## Answer checks

| Strategy | Answer checks | Service errors |
|---|---:|---:|
| Recursive | 15/15 (earlier k=20 run) | 0 |
| Markdown | Not run; retrieval only | 0 |
| Parent-child | 15/15 (fresh live run) | 0 |

These are phrase-and-citation-ID checks on a development set, not independent semantic accuracy. Manual review still found an unnecessary historical citation in parent-child POL-01; see the note in its answer report.

## Review the individual questions

[Recursive retrieval](chunking-recursive-retrieval.md) · [Markdown retrieval](chunking-markdown-retrieval.md) · [Parent-child retrieval](chunking-parent-child-retrieval.md)

[Recursive answers](chunking-recursive-answers.md) · [Parent-child answers](chunking-parent-child-answers.md)

## Selection

Parent-child is the default for this corpus because it provides more complete clauses and stronger top-five chunk recall. No source policies, golden answers, or prompt rules were changed.

To reproduce: index Markdown or parent-child with `python -m src --ingest --chunk-strategy STRATEGY --namespace NAMESPACE`, then run `python -m scripts.evaluate --namespace NAMESPACE --retrieval-only --top-k 20`. Omit `--retrieval-only` to check generated answers.
