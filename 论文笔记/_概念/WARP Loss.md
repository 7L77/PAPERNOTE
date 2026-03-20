---
type: concept
aliases: [Weighted Approximate-Rank Pairwise, WARP]
---

# WARP Loss

## Intuition

WARP Loss is a weighted pairwise ranking loss: it punishes ranking violations, and gives larger penalties when violations happen on more important (higher-rank) items.

## Why It Matters

In NAS, we mainly care about finding top architectures. WARP directly biases optimization toward better top-ranking behavior.

## Tiny Example

If architecture A should rank above B but is predicted below, WARP applies a penalty. If A is near the very top, the penalty weight is larger.

## Definition

A common form is:
\[
\mathcal{L}_{WARP}=\sum_i\sum_{j\in\mathcal{N}_i}L(rank_i)\cdot\max(0,1-\hat{y}_i+\hat{y}_j)
\]
where \(L(rank_i)\) is a rank-dependent weight.

## Math Form (if needed)

- \(\hat{y}_i\): predicted score of sample \(i\).
- \(\mathcal{N}_i\): negatives paired with \(i\).
- \(L(rank_i)\): increasing weight when item \(i\) should be ranked very high.

## Key Points

1. WARP is pairwise but rank-weighted.
2. It is top-oriented and often strong on head metrics.
3. It can be sensitive to sampling strategy and predictor capacity.

## How This Paper Uses It

- [[PWLNAS]]: introduces WARP into predictor-based NAS and uses it in piecewise settings (e.g., NAS-Bench-101 and TransNAS tasks).

## Representative Papers

- [[PWLNAS]]: reports strong top-ranking behavior of WARP in several settings.

## Related Concepts

- [[Pairwise Ranking Loss]]
- [[Piecewise Loss Function]]
