---
type: concept
aliases: [Robust NAS, Robustness-aware NAS]
---

# Robust Neural Architecture Search

## Intuition
Robust NAS searches for architectures that are not only accurate on clean data but also stable under adversarial or shifted inputs.

## Why It Matters
In many applications, a highly accurate but fragile model is not deployable. Robustness must be part of architecture design.

## Tiny Example
A cell architecture with slightly lower clean accuracy but much higher PGD robustness can be preferable in safety-critical deployment.

## Definition
Robust NAS is NAS with robustness-aware objectives, constraints, or multi-objective optimization, where architecture quality includes adversarial/corruption performance.

## Key Points
1. Robustness objectives usually increase evaluation cost.
2. Multi-objective setup (clean + robust) is common.
3. Cheap predictors (e.g., ZCP combinations) are useful for scaling robust search.

## How This Paper Uses It
- [[ZCP-Eval]]: Evaluates whether classic ZCPs can serve as robust-performance predictors.

## Representative Papers
- [[ZCP-Eval]]: Shows robust prediction is harder and needs multi-feature fusion.
- [[Adversarially Robust Architecture Search]]: Early robust-NAS direction.

## Related Concepts
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]

