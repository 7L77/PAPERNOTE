---
type: concept
aliases: [SVD, Matrix Factorization by Singular Values]
---

# Singular Value Decomposition

## Intuition
SVD rewrites a matrix as rotations plus axis-wise stretching. It separates "direction" and "strength" of variation, so we can see how much independent information a matrix carries.

## Why It Matters
In deep learning diagnostics, SVD helps quantify rank, conditioning, redundancy, and signal collapse in feature maps or Jacobians.

## Tiny Example
If one singular value is huge and others are near zero, most information lies in one direction. The representation is effectively low-rank and can be fragile.

## Definition
For matrix \(X \in \mathbb{R}^{m\times n}\), SVD is:
\[
X = U \Sigma V^\top
\]
where \(U,V\) are orthonormal, and \(\Sigma\) contains nonnegative singular values \(\sigma_1 \ge \sigma_2 \ge \dots\).

## Math Form (if needed)
- Condition number: \(c(X)=\sigma_{\max}(X)/\sigma_{\min}(X)\).
- Inverse condition signal used by many proxies: \(\sigma_{\min}/\sigma_{\max}=1/c(X)\).

## Key Points
1. Singular values reveal effective dimensionality and stability.
2. Large condition number indicates near-collinearity or ill-conditioning.
3. SVD-based metrics are label-free and easy to compute on activations.

## How This Paper Uses It
- [[Dextr]]: computes per-layer singular-value ratios (inverse condition signal) from feature maps, then sums and log-transforms them as the C/G term.

## Representative Papers
- [[Dextr]]: uses SVD and curvature fusion for zero-shot NAS.
- [[W-PCA]]: uses eigen/spectral structure for training-free ranking signals.

## Related Concepts
- [[Condition Number]]
- [[Gram Matrix]]
- [[Network Expressivity]]

