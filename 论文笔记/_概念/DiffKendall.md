---
type: concept
aliases: [Differentiable Kendall Tau, Diff Kendall]
---

# DiffKendall

## Intuition
DiffKendall is a differentiable approximation of Kendall's Tau that lets us optimize ranking quality with gradient descent.

## Why It Matters
Classic Kendall Tau is non-differentiable, so we cannot directly use it as a training objective in neural predictors.

## Tiny Example
If two architectures should be ranked A > B, DiffKendall gives a smooth reward when predicted scores satisfy this order, instead of a hard sign-only jump.

## Definition
DiffKendall replaces the sign comparisons in Kendall Tau with a smooth sigmoid-based function, then computes averaged concordance over all pairs.

## Math Form (if needed)
\[
\tau_d = \frac{1}{\binom{L}{2}}\sum_{i\neq j}\sigma_\alpha(\Delta x_{ij})\sigma_\alpha(\Delta y_{ij})
\]
where \(\sigma_\alpha\) is a smooth approximation to sign.

## Key Points
1. Directly optimizes ranking consistency.
2. Works with standard gradient-based training.
3. Sensitive to smoothing parameter alpha.

## How This Paper Uses It
- [[ParZC]]: Uses DiffKendall as the core ranking loss (Sec. 3.3, Tab. 8).

## Representative Papers
- [[ParZC]]: Adopts DiffKendall to improve zero-cost proxy-based ranking.

## Related Concepts
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
- [[Zero-Cost Proxy]]
