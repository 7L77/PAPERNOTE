---
type: concept
aliases: [Nonlinear Rank Aggregation, Rank Aggregation]
---

# Non-linear Ranking Aggregation

## Intuition
Instead of averaging scores linearly, non-linear aggregation penalizes weak dimensions more strongly, so a candidate must be good across all metrics.

## Why It Matters
In NAS, one proxy can miss critical failure modes. Non-linear aggregation prevents a bad proxy from being hidden by other good proxies.

## Tiny Example
If a model ranks very high on three proxies but very low on one, linear sum may still look good; non-linear sum of log-ranks drops it more sharply.

## Definition
A ranking fusion strategy that combines per-metric ranks with a non-linear function (e.g., logarithm) to emphasize balanced high rankings.

## Math Form (if needed)
AZ-NAS uses:
\[
s(i)=\sum_m \log(\mathrm{Rank}_m(i)/N)
\]

## Key Points
1. Encourages consistency across multiple metrics.
2. Reduces compensation effect in linear fusion.
3. Often improves robustness of ranking-based selection.

## How This Paper Uses It
- [[AZ-NAS]]: Uses log-rank summation across `sE/sP/sT/sC` to produce final AZ scores.

## Representative Papers
- Lee and Ham, AZ-NAS (CVPR 2024).

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Kendall's Tau]]

