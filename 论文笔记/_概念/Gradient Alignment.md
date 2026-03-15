---
type: concept
aliases: [Gradient Consistency, Gradient Direction Alignment]
---

# Gradient Alignment

## Intuition
When clean and perturbed gradients point to similar directions, multi-objective optimization is easier.

## Why It Matters
Large gradient conflicts can make models overfit one objective and hurt robust generalization.

## Tiny Example
Compute `|cos(g, g^r)|` for clean and robust gradients; higher values mean better alignment.

## Definition
Gradient alignment quantifies directional agreement between gradients from different tasks or data conditions.

## Key Points
1. It is a direct optimization-dynamics signal.
2. Absolute cosine similarity is commonly used.
3. Alignment is correlated with better joint optimization stability.

## How This Paper Uses It
- [[CRoZe]] uses layer-wise absolute cosine similarity between clean and perturbed gradients as `G_m` (Eq. 9).

## Representative Papers
- [[CRoZe]]

## Related Concepts
- [[Feature Consistency]]
- [[Parameter Consistency]]
- [[Adversarial Robustness]]
