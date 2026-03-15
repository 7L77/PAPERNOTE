---
type: concept
aliases: [Global Lipschitz Constant, Lipschitz Continuity]
---

# Lipschitz Constant

## Intuition
The Lipschitz constant measures how sensitive a function output is to input changes in the worst case.

## Why It Matters
In adversarial robustness, smaller sensitivity often means perturbations need to be stronger to change predictions.

## Tiny Example
If a classifier has local change bound `|f(x+delta)-f(x)| <= 2||delta||`, then a tiny perturbation can only change scores by at most about twice its size.

## Definition
A function `f` is Lipschitz continuous if there exists `L >= 0` such that for all `x1, x2`,
`||f(x1)-f(x2)|| <= L ||x1-x2||`. The smallest valid `L` is the Lipschitz constant.

## Math Form (if needed)
\[
\|f(x_1)-f(x_2)\| \le L\|x_1-x_2\|
\]
`L` is the worst-case amplification factor.

## Key Points
1. Smaller Lipschitz constants imply less worst-case sensitivity.
2. Layer/operator bounds can be composed to estimate network-level bounds.
3. Tight bounds are hard; practical methods often use approximations.

## How This Paper Uses It
- [[RACL]]: Uses a probabilistic upper-bound constraint on network Lipschitz constant to guide robust architecture sampling.

## Representative Papers
- Parseval Networks and related spectral regularization papers connect Lipschitz control to robustness.

## Related Concepts
- [[Spectral Norm]]
- [[Adversarial Robustness]]
- [[Differentiable Architecture Search]]
