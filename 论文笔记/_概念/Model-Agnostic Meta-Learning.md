---
type: concept
aliases: [MAML, First-Order MAML]
---

# Model-Agnostic Meta-Learning

## Intuition
MAML learns an initialization that can adapt to a new task with only a few gradient steps.

## Why It Matters
It is a foundational method in few-shot learning because it directly optimizes for fast adaptation.

## Tiny Example
Train on many 5-way classification tasks so that, on a new 5-way task, one or two updates already give good accuracy.

## Definition
MAML solves a bi-level objective: inner updates on support data, outer updates on query loss after adaptation.

## Math Form (if needed)
`theta' = theta - alpha * grad_theta L_support(theta)`
`min_theta sum_t L_query^t(theta'_t)`

## Key Points
1. Inner loop adapts; outer loop optimizes adaptation quality.
2. Can involve second-order gradients.
3. Widely used as a meta-learning baseline.

## How This Paper Uses It
- [[IBFS]]: Analyzes MAML-style convergence and motivates first-order architecture scoring for few-shot NAS.

## Representative Papers
- Finn et al. (2017): Original MAML.
- [[IBFS]]: Extends the perspective toward training-free NAS scoring.

## Related Concepts
- [[Few-shot Learning]]
- [[Reptile]]
- [[Neural Tangent Kernel]]
