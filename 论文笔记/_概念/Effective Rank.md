---
type: concept
aliases: [erank, Effective Dimensionality]
---

# Effective Rank

## Intuition
`Effective rank` measures how many dimensions are meaningfully used by a matrix transformation, not just how many dimensions are mathematically non-zero.

## Why It Matters
Two matrices can have the same algebraic rank but very different geometry:
- one dominated by a single direction (collapsed representation),
- one balanced across many directions (richer representation).

Effective rank distinguishes these cases.

## Tiny Example
If a layer's activation matrix has one very large singular value and all others tiny, standard rank may still be full, but effective rank is low.  
If singular values are more even, effective rank is higher.

## Definition
Given singular values `\sigma_k` of matrix `A`, define
\[
p_k = \frac{\sigma_k}{\sum_i \sigma_i}, \quad
H(p) = -\sum_k p_k \log p_k, \quad
\mathrm{erank}(A)=\exp(H(p)).
\]

## Key Points
1. Entropy over normalized singular values gives a smooth dimensionality notion.
2. Sensitive to spectral imbalance, not only zero/non-zero cutoff.
3. Useful for diagnosing representation collapse and diversity.

## How This Paper Uses It
- [[NEAR]]: sums effective ranks of pre-activation and post-activation matrices across layers as a zero-cost performance proxy.

## Representative Papers
- Roy and Vetterli, "The effective rank: A measure of effective dimensionality" (2007).
- Husistein et al., "NEAR" (ICLR 2025).

## Related Concepts
- [[Network Expressivity]]
- [[Zero-Cost Proxy]]
- [[Spectral Norm]]

