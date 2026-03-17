---
type: concept
aliases: [RL, Sequential Decision Making]
---

# Reinforcement Learning

## Intuition
Reinforcement Learning trains an agent by trial and error: it takes actions, gets rewards, and gradually learns which action sequences are better.

## Why It Matters
Many optimization/search problems are naturally sequential. RL handles this directly and can optimize long-term outcomes instead of only one-step predictions.

## Tiny Example
A maze agent gets `+1` at the exit and `0` elsewhere. At first it moves randomly; over time it learns paths that reach the exit faster.

## Definition
RL solves a Markov Decision Process (MDP): states `s`, actions `a`, transitions, rewards `r`, and policy `pi(a|s)` that maximizes expected cumulative reward.

## Math Form (if needed)
The return at time `t` is:
`G_t = sum_{k=0..infinity} gamma^k r_{t+k+1}`
where `gamma` discounts future rewards.

## Key Points
1. RL optimizes delayed rewards, not only immediate labels.
2. Exploration vs exploitation is central.
3. Value-based and policy-based methods are common families.

## How This Paper Uses It
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: uses RL as the controller for iterative NAS architecture editing.

## Representative Papers
- Mnih et al., 2015 (DQN): deep value-based RL at scale.
- Horgan et al., 2018 (Ape-X): distributed prioritized replay RL.

## Related Concepts
- [[Ape-X]]
- [[Prioritized Experience Replay]]

