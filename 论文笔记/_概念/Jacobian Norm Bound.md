---
type: concept
aliases: [Jacobian Bound, Jacobian-based Robustness Bound]
---

# Jacobian Norm Bound

## Intuition

If small input perturbations only cause small output changes, the model is locally robust. Jacobian norm quantifies this sensitivity.

## Why It Matters

It gives a differentiable proxy for robustness that is much cheaper than full certified-bound propagation, so it is practical inside architecture search loops.

## Tiny Example

For two models around the same input, if model A has smaller Jacobian norm than model B, then the same tiny perturbation tends to induce a smaller output drift in A.

## Definition

For network output `f(x)`, first-order expansion gives:
`f(x+delta) - f(x) ≈ J(x) delta`.
Using norm inequalities, output shift can be upper bounded by Jacobian row norms times perturbation radius.

## Math Form (if needed)

A common bound form is:

\[
\frac{1}{K}\sum_{k=1}^{K}|f_k(x+\delta)-f_k(x)|
\le
\frac{1}{K}\sum_{k=1}^{K}\|J_k(x)\|_q \cdot \|\delta\|_p
\]

with \(1/p + 1/q = 1\). Smaller Jacobian norms imply better local stability.

## Key Points

1. It is usually a first-order/local robustness proxy.
2. It is computationally efficient and differentiable.
3. It may be less tight than certified global bounds.

## How This Paper Uses It

- [[DSRNA]]: Defines Jacobian-norm-based lower bound as robustness metric for DSRNA-Jacobian and DSRNA-Combined.

## Representative Papers

- [[Jacobian Adversarially Regularized Networks for Robustness]]: Uses Jacobian regularization to improve adversarial robustness.

## Related Concepts

- [[Adversarial Robustness]]
- [[Certified Robustness Lower Bound]]
