---
type: concept
aliases: [Softmax Sampling, Gibbs Sampling in NAS]
---

# Boltzmann Sampling

## Intuition
Boltzmann sampling turns scores into probabilities with a temperature: high temperature explores broadly, low temperature concentrates on high-score options.

## Why It Matters
It is a simple mechanism to control exploration-exploitation smoothly in NAS and other search problems.

## Tiny Example
If two architectures have close rewards, high temperature samples both often; after annealing, the better one is selected much more frequently.

## Definition
Given rewards `r_i`, sample option `i` with
\[
p_i = \frac{\exp(r_i/T)}{\sum_j \exp(r_j/T)}.
\]

## Key Points
1. `T` controls distribution sharpness.
2. Annealing schedule is important for convergence.
3. Flat Boltzmann over huge spaces can still be expensive.

## How This Paper Uses It
- [[MCTS-Learned Hierarchy]] applies Boltzmann sampling among sibling nodes at each tree level (Eq.2), not over the full flat architecture set.

## Representative Papers
- Cesa-Bianchi et al. (2017): Boltzmann exploration analysis.
- Su et al. (2021a): MCTS-based NAS with Boltzmann-style selection.

## Related Concepts
- [[Monte-Carlo Tree Search]]
- [[Upper Confidence Bound (UCB)]]
- [[Neural Architecture Search]]
