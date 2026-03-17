---
type: concept
aliases: [Kernel Gram Matrix, Feature Similarity Matrix]
---

# Gram Matrix

## Intuition
A Gram matrix stores pairwise inner products between vectors. It tells how similar samples/features are in a chosen representation space.

## Why It Matters
Its spectrum (especially the minimum eigenvalue) is closely related to optimization dynamics and generalization analysis in kernel/NTK-style theory.

## Tiny Example
If many feature vectors are nearly parallel, pairwise inner products become similar and Gram matrix can become near-singular; this usually indicates low diversity.

## Definition
For vectors \(x_1,\dots,x_n\), Gram matrix \(G\in\mathbb{R}^{n\times n}\) is:
\[
G_{ij}=x_i^\top x_j
\]
More generally, \(G_{ij}=k(x_i,x_j)\) for kernel \(k\).

## Math Form (if needed)
- PSD property: \(G \succeq 0\).
- Small \(\lambda_{\min}(G)\) implies weakly separated directions / poor conditioning.

## Key Points
1. Gram matrix summarizes pairwise geometry in compact form.
2. Eigenvalues reveal rank, diversity, and conditioning.
3. It connects representation quality and trainability in many NAS proxies.

## How This Paper Uses It
- [[Dextr]]: theoretical motivation references Gram/NTK eigenvalue side for convergence and generalization linkage, then approximates this behavior through feature conditioning.

## Representative Papers
- [[Dextr]]: links Gram-eigenvalue intuition to practical SVD-based layer scoring.
- [[Neural Tangent Kernel]]: uses Gram-style kernel matrices for training dynamics analysis.

## Related Concepts
- [[Condition Number]]
- [[Singular Value Decomposition]]
- [[Neural Tangent Kernel]]

