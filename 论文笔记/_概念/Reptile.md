---
type: concept
aliases: [First-Order Meta-Learning]
---

# Reptile

## Intuition
Reptile is a simple meta-learning algorithm that repeatedly moves initialization parameters toward task-adapted parameters.

## Why It Matters
It avoids second-order derivatives and is often easier to implement than full MAML.

## Tiny Example
For each sampled task, train a few SGD steps to get `phi_t`, then update meta-parameters toward `phi_t`.

## Definition
Reptile performs first-order meta-updates by averaging task-specific adaptation directions.

## Math Form (if needed)
`theta <- theta + epsilon * (phi_t - theta)`
where `phi_t` is obtained by a few gradient steps on task `t`.

## Key Points
1. First-order approximation to fast-adaptation meta-learning.
2. Lower memory/compute cost than second-order methods.
3. Works well as a practical few-shot baseline.

## How This Paper Uses It
- [[IBFS]]: Uses Reptile in preliminaries as a first-order meta-learning reference for few-shot settings.

## Representative Papers
- Nichol et al. (2018): Reptile.
- [[IBFS]]: Discusses first-order adaptation context in FSL.

## Related Concepts
- [[Model-Agnostic Meta-Learning]]
- [[Few-shot Learning]]
