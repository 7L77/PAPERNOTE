---
type: concept
aliases: [lambda_min of correlation, correlation minimum eigenvalue]
---

# Minimum Eigenvalue of Correlation

## Intuition
Given a correlation matrix, the minimum eigenvalue tells us how close the representation is to collapsing along some direction. A larger minimum eigenvalue usually means the correlation structure is less degenerate.

## Why It Matters
In training-free NAS proxies like MeCo, this quantity is used as a cheap spectral signal for architecture ranking quality.

## Tiny Example
If two candidate architectures produce layer correlation matrices `P1` and `P2`, and `lambda_min(P1)` is consistently larger across layers, MeCo tends to rank architecture 1 higher.

## Definition
For a symmetric correlation matrix `P`, the minimum eigenvalue is:

$$
\lambda_{min}(P) = \min_i \lambda_i(P)
$$

where `lambda_i(P)` are eigenvalues of `P`.

## Key Points
1. It is sensitive to near-singular correlation structure.
2. Numerical stability matters when sample size is very small.
3. As a proxy term, it is often combined across layers.

## How This Paper Uses It
- [[MeCo]] defines:
  `S_MeCo = sum_l lambda_min(P(F_l(X)))`
  using one random input forward pass.

## Representative Papers
- [[MeCo]]

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Spearman's Rank Correlation]]
