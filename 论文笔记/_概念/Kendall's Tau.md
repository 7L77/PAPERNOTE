---
type: concept
aliases: [Kendall Tau, KT]
---

# Kendall's Tau

## Intuition
Kendall's Tau measures how similar two rankings are by checking pairwise order agreements.

## Why It Matters
NAS ranking methods care about order quality; Tau directly reflects whether predicted ranking matches ground-truth ranking.

## Tiny Example
If two architecture rankings preserve most pairwise orderings, Tau is high; if many pairs are reversed, Tau is low or negative.

## Definition
Kendall's Tau is a rank correlation coefficient defined from concordant and discordant pairs between two rankings.

## Math Form (if needed)
\[
\tau = \frac{C - D}{\binom{n}{2}}
\]
where `C` is number of concordant pairs and `D` is number of discordant pairs.

## Key Points
1. `tau=1` means identical ranking.
2. `tau=0` means weak/no rank correlation.
3. `tau<0` means opposite tendency.

## How This Paper Uses It
- [[AZ-NAS]]: Uses Kendall's Tau as the primary ranking consistency metric on NAS-Bench-201.

## Representative Papers
- Kendall, "A New Measure of Rank Correlation" (1938).

## Related Concepts
- [[NAS-Bench-201]]
- [[Non-linear Ranking Aggregation]]

