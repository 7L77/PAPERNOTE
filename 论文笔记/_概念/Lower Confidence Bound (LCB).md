---
type: concept
aliases: [LCB, Confidence Lower Bound]
---

# Lower Confidence Bound (LCB)

## Intuition
LCB is a pessimistic score: "estimated mean - uncertainty bonus". Lower LCB can indicate either poor observed reward or not enough trials.

## Why It Matters
It can force additional trials for under-sampled options, improving fairness before irreversible pruning decisions.

## Tiny Example
An operation has medium accuracy but very few trials. Its large uncertainty makes LCB low, so a method may sample it again before dropping it.

## Definition
A standard form is:
\[
\hat{r}_k - \sqrt{\frac{2\log N}{n_k}}.
\]
Lower `n_k` gives a lower bound, reflecting uncertainty.

## Math Form (if needed)
Compared with UCB, LCB flips the exploration bonus sign and is useful in conservative or fairness-oriented selection logic.

## Key Points
1. Emphasizes worst-case confidence rather than optimistic confidence.
2. Useful for "test-before-discard" style strategies.
3. Often paired with UCB for complementary roles.

## How This Paper Uses It
- [[ABanditNAS]]: Builds sampling probabilities from `softmax(-LCB)` so lower-confidence operations are sampled more before UCB-based elimination.

## Representative Papers
- Confidence-bound methods in stochastic bandits.
- ABanditNAS (arXiv 2020) as an anti-bandit usage pattern.

## Related Concepts
- [[Multi-Armed Bandit]]
- [[Upper Confidence Bound (UCB)]]
- [[ABanditNAS]]

