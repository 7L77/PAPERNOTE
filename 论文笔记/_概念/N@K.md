---
type: concept
aliases: [Top-K Best Rank, Best Rank in Top-K]
---

# N@K

## Intuition

N@K asks: among the top-K candidates selected by predictor scores, what is the best true rank? Lower is better.

## Why It Matters

NAS often evaluates only a shortlist due to budget constraints. If N@K is small, the shortlist likely contains near-optimal architectures.

## Tiny Example

If your predicted top-10 set contains the true global rank-2 architecture as its best member, then N@10 = 2.

## Definition

Let \(X_K\) be architectures with top-K predicted scores, and \(r_i\) be true rank:
\[
N@K=\min_{x_i\in X_K} r_i
\]

## Math Form (if needed)

- \(X_K\): predictor-selected top-K set.
- \(r_i\): true rank in full search space.
- Smaller N@K means better chance of finding high-quality architecture under budget.

## Key Points

1. It is a head-focused metric for budgeted search.
2. Unlike full-list correlation, it directly reflects search outcome potential.
3. It complements [[Precision@T]] and [[Kendall's Tau]].

## How This Paper Uses It

- [[PWLNAS]]: uses N@K as a primary top-ranking metric to compare loss families and validate piecewise loss design.

## Representative Papers

- [[PWLNAS]]: reports N@10 extensively across search spaces and predictor settings.

## Related Concepts

- [[Precision@T]]
- [[Kendall's Tau]]
