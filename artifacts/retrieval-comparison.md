# Retrieval comparison: 10 vs 20 candidates

Same 15 development questions, same recursive index (200 tokens / 40 overlap), same reranker and 4,000-token evidence budget. The gold set and recall@5 cutoff were unchanged.

| Metric | k=10 per search | k=20 per search |
|---|---:|---:|
| Candidate pool recall | 77.8% | 96.7% |
| Recall@5 | 54.4% | 54.4% |
| Final context recall | 77.8% | 96.7% |
| Answer checks (one fresh run each) | 93.3% | 100.0% |

Increasing candidates recovered more expected evidence but did not move it into the top five. This improves context coverage, not top-five ranking. The prior answer failure was a phrase-match false negative, so the answer-score difference is not evidence of a semantic improvement.

## Questions

| ID | Context recall: k=10 | Context recall: k=20 | Missing at k=20 |
|---|---:|---:|---|
| POL-01 | 100% | 100% | None |
| POL-02 | 100% | 100% | None |
| POL-03 | 100% | 100% | None |
| POL-04 | 100% | 100% | None |
| POL-05 | 0% | 100% | None |
| POL-06 | 100% | 100% | None |
| POL-07 | 100% | 100% | None |
| POL-08 | 50% | 100% | None |
| POL-09 | 100% | 100% | None |
| POL-10 | 50% | 100% | None |
| POL-11 | 100% | 100% | None |
| POL-12 | 100% | 100% | None |
| POL-13 | 0% | 50% | NS-CAUSE-2026#3.2 |
| POL-14 | 67% | 100% | None |
| POL-15 | 100% | 100% | None |

## Review the answers

[k=10 answers](evaluation-k10.md) · [k=20 answers](evaluation-k20.md)

The k=20 run passed 15/15 phrase-and-citation-ID checks with zero service errors. These are development-set checks, not independent semantic grading. POL-02 still includes an unnecessary historical citation; see its review note. Full retrieved text is available in the matching JSON files.
