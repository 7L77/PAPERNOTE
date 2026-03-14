---
type: concept
aliases: [RSP]
---

# Robust Search Primitive

## Intuition
A robust search primitive is a local architecture choice `(edge, operation)` that repeatedly appears when adversarial robustness improves across nearby searched architectures.

## Why It Matters
It turns robust NAS from a pure black-box objective into interpretable structure-level reasoning: we can point to concrete primitives that are likely responsible for robustness gains.

## Tiny Example
If architecture `A_{i+1}` is more robust than `A_i` and differs by only one primitive, that changed primitive becomes a strong robustness candidate.

## Definition
Under REP, primitives are sampled from adjacent architecture comparisons using robustness trends, then filtered by intersection across opposite trend sets (`B1` and `B2`) to produce robust primitives.

## Key Points
1. Primitive-level analysis is finer-grained than only comparing full architectures.
2. Adjacent-architecture comparison reduces confounding changes.
3. Robust primitives are used as priors, not as the only allowed primitives.

## How This Paper Uses It
- [[REP]] defines robust search primitives and uses them to build an indicator matrix `alpha_R` for probability enhancement search.

## Representative Papers
- [[REP]]: Introduces robust primitive sampling + distance-regularized differentiable NAS.

## Related Concepts
- [[Robust Neural Architecture Search]]
- [[Probability Enhancement Search Strategy]]
- [[Cell-based Search Space]]
- [[Adversarial Robustness]]
