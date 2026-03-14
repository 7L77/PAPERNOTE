---
type: concept
aliases: [NAS, Automated Architecture Design]
---

# Neural Architecture Search

## Intuition
Neural Architecture Search (NAS) is the process of letting algorithms, rather than humans, design neural network structures.

## Why It Matters
Manual architecture design is expensive and task-specific. NAS can find high-performing designs faster and sometimes beyond human intuition.

## Tiny Example
Instead of handpicking "Conv3x3 -> Conv5x5 -> Pool", NAS searches many candidates and keeps the one with best validation accuracy under a compute budget.

## Definition
NAS optimizes over a predefined architecture search space using a search strategy (e.g., evolutionary, RL, gradient-based) with an evaluation strategy (full training, one-shot, surrogate).

## Key Points
1. NAS has three parts: search space, search strategy, performance estimation.
2. Search cost is often the bottleneck.
3. Practical NAS usually trades exactness for speed (weight sharing, surrogate scoring).

## How This Paper Uses It
- [[LLMENAS]]: Uses LLM-guided evolutionary operators to improve candidate generation quality in NAS.
- [[AZ-NAS]]: Uses a training-free multi-proxy evolutionary workflow for architecture ranking and selection.

## Representative Papers
- [[DARTS]]: Differentiable NAS with continuous relaxation.
- [[AmoebaNet]]: Evolutionary NAS at scale.

## Related Concepts
- [[Evolutionary Neural Architecture Search]]
- [[One-shot NAS]]
- [[Surrogate Predictor]]
