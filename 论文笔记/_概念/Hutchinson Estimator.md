---
type: concept
aliases: [Hutchinson's Method, Random Trace Estimator]
---

# Hutchinson Estimator

## Intuition
Hutchinson Estimator approximates expensive matrix quantities using random vectors, avoiding explicit full-matrix construction.

## Why It Matters
In deep models, exact Jacobian/Hessian computation is costly. Randomized estimators give useful approximations much faster.

## Tiny Example
To estimate properties of a Jacobian-like matrix, sample Rademacher vectors and average transformed products rather than building the full matrix.

## Definition
A stochastic estimator that uses random vectors (often Rademacher) to approximate traces or matrix-related statistics.

## Math Form (if needed)
For symmetric `A`, with random `v` such that `E[vv^T]=I`, we have:
\[
E[v^TAv]=\mathrm{tr}(A)
\]

## Key Points
1. Converts high-cost matrix computation into repeated vector products.
2. Accuracy improves with more samples.
3. Widely used in large-scale deep learning approximations.

## How This Paper Uses It
- [[AZ-NAS]]: Uses Rademacher-vector backprop signals to approximate Jacobian-related quantities for the trainability proxy.

## Representative Papers
- Avron and Toledo, JACM 2011.

## Related Concepts
- [[Spectral Norm]]
- [[Zero-Cost Proxy]]

