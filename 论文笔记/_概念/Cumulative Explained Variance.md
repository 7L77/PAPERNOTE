---
type: concept
aliases: [CEV, Explained Variance Threshold]
---

# Cumulative Explained Variance

## Intuition

It tells how much total information is covered when keeping the first `k` principal components.

## Why It Matters

It provides a practical stopping rule for dimensionality selection in PCA-based pipelines.

## Tiny Example

If top 20 components explain 95% variance, then using 20 dimensions is often enough for downstream comparison.

## Definition

For sorted PCA eigenvalues `lambda_1 ... lambda_D`, cumulative explained variance at `k` is:
`sum_{i=1..k} lambda_i / sum_{i=1..D} lambda_i`.

## Math Form (if needed)

Select minimum `k` such that cumulative ratio `>= eta`, where `eta` is a threshold like 0.99.

## Key Points

1. It converts eigenvalue spectrum into an interpretable scalar criterion.
2. Higher `eta` keeps more information but also more dimensions.
3. Different models can be compared by required `k` at same `eta`.

## How This Paper Uses It

- [[W-PCA]]: Defines PCA_dim as the minimum principal-component count whose cumulative contribution exceeds `eta`.

## Representative Papers

- [[W-PCA]]: Uses `eta`-based PCA_dim in zero-shot architecture scoring.

## Related Concepts

- [[Principal Component Analysis]]
- [[Zero-Cost Proxy]]
