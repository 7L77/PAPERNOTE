---
type: concept
aliases: [Weight-sharing NAS, Supernet NAS]
---

# One-shot NAS

## Intuition
Instead of training every candidate architecture from scratch, train one over-parameterized supernet once and reuse shared weights to evaluate many sub-architectures quickly.

## Why It Matters
It reduces NAS search time by orders of magnitude and makes large search spaces practical.

## Tiny Example
Train a supernet containing both `3x3 conv` and `5x5 conv` branches; evaluate a candidate by activating one branch path without retraining from zero.

## Definition
One-shot NAS is a weight-sharing NAS paradigm where candidate architectures are treated as subnetworks of a common supernet.

## Key Points
1. Very efficient but introduces weight-sharing bias.
2. Ranking quality may differ from full retraining quality.
3. Commonly paired with additional predictors or re-ranking.

## How This Paper Uses It
- [[LLMENAS]]: Uses one-shot style fast evaluation as part of the search loop to reduce compute cost.

## Representative Papers
- [[ENAS]]: Early parameter-sharing NAS.
- [[DARTS]]: Continuous relaxation with shared weights.

## Related Concepts
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
- [[Evolutionary Neural Architecture Search]]

