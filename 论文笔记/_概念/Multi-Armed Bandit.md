---
type: concept
aliases: [MAB, Bandit Problem]
---

# Multi-Armed Bandit

## Intuition
You repeatedly choose among several options ("arms"), each with uncertain payoff, and must balance trying new arms vs exploiting known good arms.

## Why It Matters
It formalizes exploration-exploitation tradeoffs in sequential decision making under limited budget.

## Tiny Example
A recommendation system can show familiar popular content (exploit) or occasionally new content (explore) to learn user preference.

## Definition
The multi-armed bandit problem is an online decision process where, at each round, an agent selects one arm and observes a stochastic reward, aiming to maximize cumulative reward (or minimize regret).

## Math Form (if needed)
A common objective is minimizing regret:
\[
R_T = \sum_{t=1}^T \big(\mu^\* - \mu_{a_t}\big),
\]
where `mu*` is the best arm mean reward and `mu_{a_t}` is the chosen arm mean at round `t`.

## Key Points
1. Feedback is partial: only chosen-arm reward is observed.
2. Exploration is necessary to avoid local traps.
3. Many practical algorithms are confidence-bound or Thompson-sampling based.

## How This Paper Uses It
- [[ABanditNAS]]: Treats edge-operation selection in NAS as a huge-armed bandit and modifies UCB/LCB usage for efficient pruning.

## Representative Papers
- Auer et al., "Finite-time Analysis of the Multiarmed Bandit Problem" (2002): UCB analysis foundation.
- Kocsis and Szepesvari, "Bandit based Monte-Carlo planning" (2006): bandit principle in tree search.

## Related Concepts
- [[Upper Confidence Bound (UCB)]]
- [[Lower Confidence Bound (LCB)]]
- [[Neural Architecture Search]]

