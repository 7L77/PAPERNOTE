---
type: concept
aliases: [Distributed Prioritized Experience Replay, Ape-X DQN]
---

# Ape-X

## Intuition
Ape-X is a distributed RL setup where many workers collect experience in parallel and a centralized learner updates the network from prioritized replay.

## Why It Matters
It greatly increases throughput for experience collection and can speed up large-scale RL training.

## Tiny Example
Instead of one agent-environment loop, 32 workers gather trajectories simultaneously and push them to one shared prioritized replay buffer.

## Definition
Ape-X (Horgan et al., 2018) is a distributed architecture for value-based RL, typically built on DQN variants, combining asynchronous actors and centralized prioritized replay learning.

## Math Form (if needed)
Sampling probability for transition `i` under prioritized replay:
`P(i) = p_i^alpha / sum_k p_k^alpha`
with importance correction using `beta`.

## Key Points
1. Parallel actors increase data throughput.
2. Central learner updates from prioritized replay data.
3. Throughput improves, but sample efficiency can still be a concern.

## How This Paper Uses It
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: uses Ape-X-style training to optimize RL-NAS agents across source and target tasks.

## Representative Papers
- Horgan et al., 2018: Distributed Prioritized Experience Replay.
- Schaul et al., 2016: Prioritized Experience Replay.

## Related Concepts
- [[Reinforcement Learning]]
- [[Prioritized Experience Replay]]

