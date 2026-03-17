---
type: concept
aliases: [PER, Prioritized Replay]
---

# Prioritized Experience Replay

## Intuition
Instead of sampling past transitions uniformly, prioritize transitions that are more informative (often higher TD error).

## Why It Matters
RL training can waste updates on low-information samples. Prioritization focuses learning on transitions that may produce larger policy/value improvements.

## Tiny Example
If a transition has large prediction error, replaying it more often helps the network quickly correct that mistake.

## Definition
PER samples transition `i` with probability proportional to its priority `p_i`, usually derived from TD error magnitude.

## Math Form (if needed)
Sampling distribution:
`P(i) = p_i^alpha / sum_k p_k^alpha`
Importance-sampling weight:
`w_i = (1 / (N * P(i)))^beta`

## Key Points
1. `alpha` controls prioritization strength.
2. `beta` corrects sampling bias during optimization.
3. Better learning speed is common, but noisy priorities can destabilize updates.

## How This Paper Uses It
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: uses PER with replay capacity `25k`, `alpha=0.6`, `beta=0.4` in RL-NAS training.

## Representative Papers
- Schaul et al., 2016: Prioritized Experience Replay.
- Horgan et al., 2018: Ape-X.

## Related Concepts
- [[Ape-X]]
- [[Reinforcement Learning]]

