---
type: concept
aliases: [Operator Norm, Largest Singular Value]
---

# Spectral Norm

## Intuition
Spectral norm measures how much a linear map can maximally stretch an input vector.

## Why It Matters
For gradient flow analysis, spectral norms near 1 are often associated with more stable propagation (less exploding/vanishing).

## Tiny Example
If a layer Jacobian has spectral norm 3, some gradient directions can be amplified about 3x in one step.

## Definition
For matrix `A`, spectral norm is its largest singular value: `||A||_2 = sigma_max(A)`.

## Math Form (if needed)
\[
\|A\|_2 = \max_{\|x\|_2=1}\|Ax\|_2 = \sigma_{\max}(A)
\]

## Key Points
1. Captures worst-case amplification factor.
2. Central in stability and Lipschitz analyses.
3. Often approximated in deep networks for efficiency.

## How This Paper Uses It
- [[AZ-NAS]]: Uses Jacobian spectral norm surrogates to form the trainability proxy `sT`.

## Representative Papers
- Pennington et al., analyses of dynamical isometry and trainability.

## Related Concepts
- [[Hutchinson Estimator]]
- [[Training-free NAS]]

