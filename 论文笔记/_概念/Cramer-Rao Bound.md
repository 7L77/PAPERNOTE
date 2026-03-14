---
type: concept
aliases: [CRB, Cramer Rao Bound]
---

# Cramer-Rao Bound

## Intuition

Cramer-Rao Bound says unbiased estimators cannot have arbitrarily small variance. The data and model information put a hard lower bound on how certain parameter estimates can be.

## Why It Matters

It gives a formal bridge from information geometry to optimization difficulty: lower available information means higher unavoidable estimation uncertainty.

## Tiny Example

If two models fit the same data but one has richer information in its parameters, its minimum achievable estimator variance is smaller, so learning can be more stable.

## Definition

For an unbiased estimator `theta_hat` with `n` samples and FIM `F(theta)`,

`Var(theta_hat) >= (1/n) * F(theta)^{-1}`.

## Math Form (if needed)

In VKDNW (Sec. II-A, Eq. (3)), the bound is used to motivate how FIM spectrum relates to uncertainty and trainability.

## Key Points

1. It is a lower bound, not an achieved variance in general finite-sample settings.
2. Larger information (larger FIM in matrix sense) implies tighter uncertainty lower bound.
3. It motivates why analyzing FIM eigenvalues can reveal optimization difficulty.

## How This Paper Uses It

- [[VKDNW]]: Uses CRB intuition to justify entropy over FIM eigenvalues as a quality signal.

## Representative Papers

- [[VKDNW]]: Applies CRB-inspired reasoning in training-free NAS proxy design.

## Related Concepts

- [[Fisher Information Matrix]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
