---
type: concept
aliases: [One-Epoch Proxy, Early-Epoch Accuracy Proxy]
---

# One-Epoch Proxy Evaluation

## Intuition
Instead of fully training every candidate model, we train only one epoch and use that early accuracy as a cheap ranking signal.

## Why It Matters
Full NAS evaluation is expensive. One-epoch proxy dramatically reduces per-candidate cost, enabling many more search iterations.

## Tiny Example
If model A gets 62% and model B gets 51% after one epoch under the same setup, A is prioritized for further search even before full convergence.

## Definition
A low-cost architecture quality estimate computed from validation/test accuracy after exactly one training epoch under fixed training protocol.

## Key Points
1. It is a ranking signal, not a final performance guarantee.
2. Works best when training settings are strictly controlled across candidates.
3. Useful for iterative search loops where throughput matters more than exact final score per step.

## How This Paper Uses It
- [[Iterative LLM-Based NAS with Feedback Memory]]: Uses one-epoch Top-1 accuracy as the core feedback metric for each generated architecture.

## Representative Papers
- [[Iterative LLM-Based NAS with Feedback Memory]]: Demonstrates iterative LLM-NAS improvement using one-epoch proxy across three datasets.

## Related Concepts
- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Spearman's Rank Correlation]]
