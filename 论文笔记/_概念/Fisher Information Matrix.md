---
type: concept
aliases: [FIM, Fisher Information]
---

# Fisher Information Matrix

## Intuition

The Fisher Information Matrix measures how sensitive a model's predicted distribution is to small parameter changes. If tiny weight changes strongly alter predictions, the model carries more information in those directions.

## Why It Matters

In optimization and estimation, FIM characterizes which parameter directions are easy or hard to estimate from data. It is a principled way to talk about trainability and uncertainty.

## Tiny Example

Imagine two network directions: in one direction prediction barely moves, in another it changes a lot. FIM gives a low value to the first and high value to the second, telling us where learning signal is informative.

## Definition

For model distribution `p_theta(y|x)`, the Fisher Information Matrix is the expectation of score outer products:

`F(theta) = E[grad_theta log p_theta(y|x) * grad_theta log p_theta(y|x)^T]`.

## Math Form (if needed)

In the VKDNW paper's notation:

`F(theta) = E[grad_theta sigma_theta(c|x) grad_theta sigma_theta(c|x)^T]` (Sec. II-A, Eq. (2), equivalent up to formulation details).

Here `theta` is model weights, `x` is input, and `c` is class variable.

## Key Points

1. FIM is positive semidefinite and spectrum-aware.
2. Its inverse links to estimator variance via [[Cramer-Rao Bound]].
3. Spectrum shape can be used as a proxy signal for trainability.

## How This Paper Uses It

- [[VKDNW]]: Builds a training-free NAS proxy from the entropy of representative FIM eigenvalues.

## Representative Papers

- [[VKDNW]]: Uses FIM spectrum entropy as a ranking signal.

## Related Concepts

- [[Cramer-Rao Bound]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
