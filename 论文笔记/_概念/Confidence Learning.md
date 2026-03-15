---
type: concept
aliases: [Uncertainty-aware Parameter Learning, Confidence-aware Optimization]
---

# Confidence Learning

## Intuition
Confidence learning treats model parameters or decisions as uncertain and learns not only what value to use, but also how certain the model is about that value.

## Why It Matters
When search/optimization is noisy or ambiguous, confidence helps avoid over-committing to unstable choices.

## Tiny Example
Two operations have similar mean score, but one has much higher variance. Confidence-aware search may prefer the lower-variance operation for stable final sampling.

## Definition
Confidence learning augments parameter learning with uncertainty estimates (e.g., variance, posterior spread, confidence bounds) and uses them in decision constraints or sampling rules.

## Math Form (if needed)
A common pattern is to optimize expected objective with uncertainty-aware constraints,
for example probability constraints like `Pr(metric <= threshold) >= eta`.

## Key Points
1. Separates value quality from certainty about that value.
2. Helps balance exploration and exploitation.
3. Often implemented with distributional parameters (mean/variance) rather than point estimates.

## How This Paper Uses It
- [[RACL]]: Learns architecture parameters as log-normal distributions and constrains robustness via confidence probability on network Lipschitz upper bound.

## Representative Papers
- Bayesian optimization and uncertainty-aware NAS works broadly use confidence-aware selection ideas.

## Related Concepts
- [[Log-normal Distribution]]
- [[Lipschitz Constant]]
- [[Differentiable Architecture Search]]
