---
type: concept
aliases: [PCA, Principal Components]
---

# Principal Component Analysis

## Intuition

PCA finds a new coordinate system where the first few directions preserve most variation in data.

## Why It Matters

It compresses high-dimensional signals into a smaller set of informative dimensions, which is useful for analysis and proxy design.

## Tiny Example

If points lie near a slanted line in 2D, PCA finds that line as PC1 and shows that one dimension already keeps most information.

## Definition

Given centered data matrix `X`, PCA computes eigenvectors of covariance `X^T X`. Ordered eigenvalues indicate variance explained by each component.

## Math Form (if needed)

If eigenvalues are `lambda_1 >= lambda_2 >= ...`, then component `k` explains ratio `lambda_k / sum_i lambda_i`.

## Key Points

1. PCA is unsupervised and label-free.
2. Eigenvalue spectrum describes information concentration.
3. Choosing top-k components is a variance-retention tradeoff.

## How This Paper Uses It

- [[W-PCA]]: Uses FFN hidden-state PCA dimensions as a training-free architecture quality signal.

## Representative Papers

- [[W-PCA]]: Uses PCA-derived dimensions for zero-shot proxy construction.

## Related Concepts

- [[Cumulative Explained Variance]]
- [[Training-free NAS]]
