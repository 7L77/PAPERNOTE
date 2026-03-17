---
type: concept
aliases: [First-order Stochastic Dominance, FSD]
---

# Stochastic Dominance

## Intuition
Stochastic dominance compares two uncertain outcomes by looking at their whole distributions, not just their means. If A stochastically dominates B, A tends to be better across thresholds.

## Why It Matters
Two methods can have similar means but very different risk profiles. Distribution-aware comparison avoids being misled by average-only summaries.

## Tiny Example
If A's scores are usually high and rarely very low, while B has the same mean but many bad-tail cases, A may stochastically dominate B even when means are close.

## Definition
For random variables `X` and `Y`, first-order stochastic dominance (`X` over `Y`) means:

\[
P(X>k)\ge P(Y>k)\ \forall k,
\]

with strict inequality for at least one `k`.

Equivalent CDF view:

\[
F_X(k)\le F_Y(k)\ \forall k
\]

with strict inequality somewhere.

## Math Form (if needed)
- `k`: performance threshold.
- If `X` dominates `Y`, then `E[X] >= E[Y]` under broad conditions, but the reverse is not always true.

## Key Points
1. Dominance is stricter than mean comparison.
2. It captures tail behavior and consistency.
3. In noisy architecture ranking, it supports safer selection decisions.

## How This Paper Uses It
- [[Variation-Matters]]: architecture comparison targets stochastic superiority via Mann-Whitney-based testing (Sec. 4.2).

## Representative Papers
- [[Variation-Matters]]: uses stochastic-ordering logic to replace average-based ranking.

## Related Concepts
- [[Mann-Whitney U Test]]
- [[Coefficient of Variation]]
- [[Kendall's Tau]]

