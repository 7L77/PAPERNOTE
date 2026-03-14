---
type: concept
aliases: [Spearman Rho, Rank Correlation]
---

# Spearman's Rank Correlation

## Intuition
This metric checks whether two lists have similar ordering, regardless of exact numeric spacing.

## Why It Matters
NAS proxy quality is usually judged by ranking consistency with true architecture performance, not absolute score values.

## Tiny Example
If architecture A > B > C in true accuracy and proxy also gives A > B > C, Spearman is high even if score magnitudes differ.

## Definition
Spearman's rho is the Pearson correlation computed on rank-transformed variables, typically in \([-1,1]\), where 1 means perfect rank agreement.

## Key Points
1. It measures monotonic relation of rankings.
2. It is robust to non-linear but order-preserving transforms.
3. It is widely used for zero-cost proxy benchmarking.

## How This Paper Uses It
- [[SWAP-NAS]]: Uses Spearman coefficients to compare SWAP-score and baselines across search spaces and tasks.

## Representative Papers
- [[SWAP-NAS]]: Reports Spearman gains from SWAP and regularized SWAP.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Kendall's Tau]]

