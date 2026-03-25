---
type: concept
aliases: [Pearson Correlation, Linear Correlation Coefficient]
---

# Pearson Correlation Coefficient

## Intuition
Pearson correlation tells us whether two vectors move in the same direction after removing their mean and normalizing variance.

## Why It Matters
When magnitudes can shift (for example after pruning), Pearson correlation can still compare directional consistency more robustly than raw dot product.

## Tiny Example
If one vector is exactly `3x + 5` of another, dot product changes a lot with scale, but Pearson correlation remains close to 1.

## Definition
For variables `x` and `y`, Pearson correlation is:
\[
\rho(x,y)=\frac{\mathrm{cov}(x,y)}{\sigma_x \sigma_y}
\]
with range `[-1, 1]`, where `1` means perfect positive linear relation and `-1` means perfect negative relation.

## Key Points
1. It is centered and variance-normalized.
2. It is invariant to affine scaling (`ax+b`) up to sign.
3. It captures linear direction agreement, not causal relation.

## How This Paper Uses It
- [[TraceNAS]] computes per-layer Pearson correlation between base and candidate gradient traces, then performs sparsity-weighted aggregation.

## Representative Papers
- [[TraceNAS]]: Uses Pearson correlation as the core alignment primitive in its zero-shot pruning proxy.

## Related Concepts
- [[Spearman's Rank Correlation]]
- [[Gradient Trace Correlation]]
- [[Gradient Alignment]]
