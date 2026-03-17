---
type: concept
aliases: [Wilcoxon rank-sum test, U-test]
---

# Mann-Whitney U Test

## Intuition
The Mann-Whitney U test asks whether values from one group tend to be larger than values from another group, using ranks instead of Gaussian assumptions.

## Why It Matters
In many ML evaluation settings, score samples are noisy and non-normal. A rank-based nonparametric test is often more robust than mean-only parametric testing.

## Tiny Example
Suppose architecture A and B each have 10 proxy scores. If A's scores are consistently ranked above B's, U-test can detect this directional advantage.

## Definition
Given two independent samples `X={x_i}` and `Y={y_j}`, compute the U statistic from rank sums. For one-sided testing:

- `H0`: two samples come from the same distribution.
- `H1`: `X` tends to be stochastically larger than `Y`.

## Math Form (if needed)
One form:

\[
U_X = R_X - \frac{n_X(n_X+1)}{2}
\]

where `R_X` is the sum of ranks in pooled samples. Smaller p-value indicates stronger evidence against `H0`.

## Key Points
1. Nonparametric and rank-based.
2. Suitable for small noisy sample comparisons.
3. Can be used one-sided when directional superiority is required.

## How This Paper Uses It
- [[Variation-Matters]]: uses one-sided U-test as the architecture comparator in `Stat-MAX` and `Stat-TOPK` (Sec. 4.2, Algorithm 1).

## Representative Papers
- [[Variation-Matters]]: applies U-test directly inside random and evolutionary NAS search decisions.

## Related Concepts
- [[Stochastic Dominance]]
- [[Coefficient of Variation]]
- [[Evolutionary Neural Architecture Search]]

