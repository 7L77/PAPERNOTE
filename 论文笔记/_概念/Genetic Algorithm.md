---
type: concept
aliases: [GA, Evolutionary Search]
---

# Genetic Algorithm

## Intuition

GA evolves a population of candidates by selection, crossover, and mutation to improve objective scores over generations.

## Why It Matters

For NAS, GA works well with non-differentiable objectives and discrete architecture encodings.

## Tiny Example

Encode each layer choice as an integer gene; keep top architectures, cross them, mutate a few positions, and iterate.

## Definition

A genetic algorithm is a population-based stochastic optimization method inspired by natural evolution.

## Math Form (if needed)

No single universal equation; core loop is:
`population_t -> selection -> crossover/mutation -> population_{t+1}` with fitness-guided survival.

## Key Points

1. Works on discrete or mixed search spaces.
2. Does not require gradient information.
3. Performance depends on encoding, fitness design, and mutation/crossover settings.

## How This Paper Uses It

- [[W-PCA]]: Uses GA to optimize architecture encoding with W-PCA score as fitness under parameter constraints.

## Representative Papers

- Regularized Evolution for Image Classifier Architecture Search (Real et al., 2019).

## Related Concepts

- [[Neural Architecture Search]]
- [[Training-free NAS]]
