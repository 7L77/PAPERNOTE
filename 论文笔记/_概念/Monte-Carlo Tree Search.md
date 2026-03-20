---
type: concept
aliases: [MCTS, Monte Carlo Tree Search]
---

# Monte-Carlo Tree Search

## Intuition
MCTS treats decision making as repeated simulations on a tree: try promising branches, but keep some exploration for uncertain branches.

## Why It Matters
It gives a practical way to optimize large discrete search spaces without exhaustively scoring every configuration.

## Tiny Example
If a search tree has many architecture branches, MCTS first samples broadly, then gradually focuses on branches that repeatedly yield better validation rewards.

## Definition
MCTS iterates four conceptual steps: selection, expansion, simulation, and backpropagation. In NAS variants with fully expanded trees, expansion/simulation may be simplified or skipped.

## Key Points
1. Balances exploration and exploitation via confidence bonuses.
2. Quality of tree structure strongly affects search efficiency.
3. Reward design and visit statistics determine convergence behavior.

## How This Paper Uses It
- [[MCTS-Learned Hierarchy]] uses MCTS on a learned architecture hierarchy and updates node rewards with UCT-style terms (Eq.2-4).

## Representative Papers
- Kocsis and Szepesvari (2006): UCT formulation.
- Wang et al. (2021a): MCTS for NAS in macro search spaces.
- Su et al. (2021a): prioritized architecture sampling with MCTS.

## Related Concepts
- [[Upper Confidence Bound (UCB)]]
- [[Multi-Armed Bandit]]
- [[Neural Architecture Search]]
- [[Boltzmann Sampling]]
