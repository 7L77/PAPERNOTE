---
type: concept
aliases: [Prediction Error Minimization, PC Learning]
---

# Predictive Coding

## Intuition
Each layer tries to predict signals from neighboring layers and learns by reducing prediction errors.

## Why It Matters
It offers a biologically motivated alternative to standard backpropagation with local error-correction dynamics.

## Tiny Example
A layer predicts top-down activity; mismatch between prediction and actual activity becomes a local error signal used to update states/weights.

## Definition
Predictive coding is a framework where neural computation is cast as iterative minimization of prediction errors across hierarchical layers, often via local update rules.

## Key Points
1. Learning is framed as error-correction rather than exact reverse-mode differentiation.
2. Iterative inference can improve stability but may increase compute.
3. Practical implementations usually add normalization, damping, or gating.

## How This Paper Uses It
- [[BioNAS]] experiments with a predictive-coding-inspired convolution operator as an additional candidate in the mixed-rule search space.

## Representative Papers
- Predictive coding literature cited as PEPITA/forward-style alternatives in BioNAS background.
- [[BioNAS]] for NAS integration context.

## Related Concepts
- [[Feedback Alignment]]
- [[Hebbian Learning]]
- [[Neural Architecture Search]]

