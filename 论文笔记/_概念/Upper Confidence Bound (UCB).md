---
type: concept
aliases: [UCB, Confidence Upper Bound]
---

# Upper Confidence Bound (UCB)

## Intuition
UCB gives each option an optimistic score: "estimated mean + uncertainty bonus". Less-tested options get larger bonus.

## Why It Matters
It is a simple and effective way to trade off exploration and exploitation with theoretical guarantees in bandit settings.

## Tiny Example
Two operations have similar observed accuracy, but one has been tried only a few times. UCB boosts the less-tested one so it is not ignored too early.

## Definition
For arm `k`, UCB at round `N` is often:
\[
\hat{r}_k + \sqrt{\frac{2\log N}{n_k}},
\]
where `hat{r}_k` is empirical mean reward and `n_k` is pull count.

## Math Form (if needed)
The uncertainty term shrinks as `n_k` grows and grows slowly with `N`, encouraging early exploration and later stabilization.

## Key Points
1. Optimism under uncertainty drives exploration.
2. Works well when rewards are bounded/sub-Gaussian.
3. In practice, constants may be tuned for task scale.

## How This Paper Uses It
- [[ABanditNAS]]: Uses UCB to prune operations with minimum UCB (anti-bandit elimination), instead of selecting maximum UCB for direct play.

## Representative Papers
- Auer et al. (2002): classic UCB derivation.
- Kocsis and Szepesvari (2006): UCB in MCTS/UCT.

## Related Concepts
- [[Multi-Armed Bandit]]
- [[Lower Confidence Bound (LCB)]]
- [[ABanditNAS]]

