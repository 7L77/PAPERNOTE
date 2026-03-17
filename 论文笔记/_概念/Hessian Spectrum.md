---
type: concept
aliases: [Hessian Eigenvalue Spectrum, Input Hessian Sharpness]
---

# Hessian Spectrum

## Intuition
Hessian spectrum describes local curvature: large top eigenvalues mean a sharper landscape and typically weaker robustness.

## Why It Matters
It provides a training-/analysis-time proxy for vulnerability: flatter local geometry is often linked with better stability under perturbations.

## Tiny Example
Think of two bowls: one steep and narrow, one wide and flat. A small push leaves the flat bowl region less easily.

## Definition
For loss `L`, Hessian `H = \nabla^2_x L` (or with respect to parameters in some settings). The largest eigenvalue `lambda_max(H)` is a curvature indicator.

## Math Form (if needed)
\[
\lambda_{\max}(H) = \max_{\|v\|_2=1} v^\top H v.
\]
Larger `lambda_max` implies sharper curvature around the evaluated point.

## Key Points
1. Spectrum summarizes sensitivity of loss to perturbations.
2. Largest eigenvalue is a practical scalar proxy.
3. Correlation with robustness can degrade in strong-attack regimes.

## How This Paper Uses It
- [[NADR-Dataset]]: Computes largest Hessian eigenvalue on all architectures and compares rank correlation with robustness rankings.

## Representative Papers
- Zhao et al., "Bridging the Gap Between Adversarial Robustness and Optimization Bias" (2020).
- Mok et al., "Hessian-based Robust NAS" (2021 line of work).

## Related Concepts
- [[Jacobian Norm Bound]]
- [[Adversarial Robustness]]
- [[NADR-Dataset]]

