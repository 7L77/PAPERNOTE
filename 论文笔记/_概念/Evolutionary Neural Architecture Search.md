---
type: concept
aliases: [Evolutionary NAS, ENAS-Evolutionary]
---

# Evolutionary Neural Architecture Search

## Intuition
Treat each architecture as an individual in a population, then evolve better models over generations using selection, crossover, and mutation.

## Why It Matters
Evolutionary search is robust to non-differentiable choices and can naturally handle discrete architecture decisions.

## Tiny Example
Keep top-performing architectures, combine parts from two parents, randomly mutate one operation, and re-evaluate offspring.

## Definition
Evolutionary NAS is a NAS strategy that optimizes architecture fitness through iterative population-based evolution under compute constraints.

## Key Points
1. Works well in discrete search spaces.
2. Quality depends heavily on crossover/mutation design.
3. Can be expensive without fast evaluators.

## How This Paper Uses It
- [[LLMENAS]]: Replaces handcrafted crossover/mutation with LLM-guided operators and combines one-shot/surrogate evaluation.

## Representative Papers
- [[AmoebaNet]]: Large-scale evolutionary architecture search.
- [[Regularized Evolution for Image Classifier Architecture Search]]: Aging evolution strategy.

## Related Concepts
- [[Neural Architecture Search]]
- [[One-shot NAS]]
- [[LLM-guided Search]]

