---
type: concept
aliases: [Output Curve Curvature, Kappa]
---

# Extrinsic Curvature

## Intuition
Extrinsic curvature tells how sharply a curve bends in ambient space. For neural networks, it measures how curved the output trajectory becomes when input moves along a controlled path.

## Why It Matters
Higher output curvature is often used as a proxy for richer function-shaping capacity, i.e., stronger expressivity.

## Tiny Example
If two models are fed the same circular input path, one may map it to an almost straight output line (low curvature), while another maps it to a twisted curve (high curvature). The latter is typically more expressive.

## Definition
Given output trajectory \(f(g(\theta))\), curvature \(\kappa(\theta)\) is computed from first and second derivatives w.r.t. \(\theta\), and aggregated along the path.

## Math Form (if needed)
A common form is based on:
\[
\kappa \propto \|v\|^{-3}\sqrt{\|v\|^2\|a\|^2-(v^\top a)^2}
\]
where \(v=\frac{d f(g(\theta))}{d\theta}\), \(a=\frac{d^2 f(g(\theta))}{d\theta^2}\).

## Key Points
1. Curvature captures output geometry, not just magnitude.
2. It can be estimated without labels.
3. Estimation usually needs higher-order autodiff, which is computationally heavier.

## How This Paper Uses It
- [[Dextr]]: uses \(\log(1+\kappa)\) as expressivity term and fuses it with inverse-condition term.

## Representative Papers
- [[Dextr]]: directly integrates extrinsic curvature in zero-shot NAS proxy.
- [[Network Expressivity]]: concept family where geometry-based complexity is used to describe representation capacity.

## Related Concepts
- [[Network Expressivity]]
- [[Singular Value Decomposition]]
- [[Gram Matrix]]

