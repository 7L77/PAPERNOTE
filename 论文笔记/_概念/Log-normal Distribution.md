---
type: concept
aliases: [Lognormal Distribution, LN Distribution]
---

# Log-normal Distribution

## Intuition
A random variable is log-normal when its logarithm is normally distributed, so the variable itself is always positive and often right-skewed.

## Why It Matters
Many multiplicative effects produce log-normal behavior, and positivity is useful when modeling quantities like scales, rates, or Lipschitz bounds.

## Tiny Example
If `Z ~ N(mu, sigma^2)` and `X = exp(Z)`, then `X` is log-normal: small values are common, but occasionally very large values appear.

## Definition
`X` is log-normal if `ln X ~ N(mu, sigma^2)`.

## Math Form (if needed)
\[
X \sim \mathrm{LN}(\mu,\sigma^2) \iff \ln X \sim \mathcal N(\mu,\sigma^2)
\]

## Key Points
1. Support is strictly positive (`X > 0`).
2. Product of independent log-normal variables remains log-normal.
3. Sum of log-normal variables has no exact closed form but can be approximated.

## How This Paper Uses It
- [[RACL]]: Models architecture parameters with log-normal distributions so sampled values stay positive and enable Lipschitz distribution propagation.

## Representative Papers
- Fenton-Wilkinson style approximations are common for sums of log-normal variables.

## Related Concepts
- [[Lipschitz Constant]]
- [[Confidence Learning]]
- [[Differentiable Architecture Search]]
