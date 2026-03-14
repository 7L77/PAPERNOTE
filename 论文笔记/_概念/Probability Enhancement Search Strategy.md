---
type: concept
aliases: [PESS, Distance-Regularized Architecture Search]
---

# Probability Enhancement Search Strategy

## Intuition
Instead of forcing the search to pick only robust primitives, this strategy softly increases their selection probability by pulling architecture parameters toward a robust-primitive indicator matrix.

## Why It Matters
It balances two goals at once: preserve natural accuracy and improve adversarial robustness.

## Tiny Example
If two operations are both robust candidates on one edge, both get probability support; the one better for validation loss can still win.

## Definition
Given architecture parameters `alpha` and robust indicator `alpha_R`, optimize:
`L_val(w*(alpha), alpha) + lambda * ||alpha - alpha_R||^2`,
with the usual bi-level training relation for `w*(alpha)`.

## Key Points
1. It is a soft bias, not hard masking.
2. Works as regularization and can reduce validation overfitting in architecture parameters.
3. Can be plugged into existing differentiable NAS optimization loops.

## How This Paper Uses It
- [[REP]] applies this strategy after robust primitive sampling, using Euclidean distance by default.

## Representative Papers
- [[REP]]: Introduces this strategy for robust differentiable NAS.

## Related Concepts
- [[Robust Search Primitive]]
- [[Robust Neural Architecture Search]]
- [[Neural Architecture Search]]
