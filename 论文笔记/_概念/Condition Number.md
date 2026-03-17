---
type: concept
aliases: [Matrix Condition Number, Numerical Conditioning]
---

# Condition Number

## Intuition
Condition number measures how sensitive outputs are to small input perturbations. A high value means tiny noise can cause large downstream changes.

## Why It Matters
It is a practical stability indicator for optimization, linear solves, and feature geometry quality.

## Tiny Example
Two almost-parallel feature vectors produce a matrix with very small \(\sigma_{\min}\), so condition number becomes large. This often implies unstable inversion and poor numerical behavior.

## Definition
For matrix \(X\), the spectral condition number is:
\[
c(X)=\frac{\sigma_{\max}(X)}{\sigma_{\min}(X)}
\]
where \(\sigma_{\max}\) and \(\sigma_{\min}\) are largest/smallest singular values.

## Math Form (if needed)
- Well-conditioned: \(c(X)\) near 1.
- Ill-conditioned: \(c(X)\) very large.
- Inverse condition measure: \(1/c(X)=\sigma_{\min}/\sigma_{\max}\).

## Key Points
1. Small \(\sigma_{\min}\) is the main source of instability.
2. Conditioning links geometry (collinearity) and optimization behavior.
3. In NAS proxies, inverse condition signals are used as "feature diversity" indicators.

## How This Paper Uses It
- [[Dextr]]: sums inverse condition contributions across layers and fuses with curvature term to form final score.

## Representative Papers
- [[Dextr]]: uses condition-number side as convergence/generalization component.
- [[MeCo]]: related line of work using spectral/correlation properties for training-free ranking.

## Related Concepts
- [[Singular Value Decomposition]]
- [[Gram Matrix]]
- [[Feature Map Collinearity]]

