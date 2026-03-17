---
type: concept
aliases: [Tensor Product of Matrices]
---

# Kronecker Product

## Intuition
Kronecker product combines two matrices into a larger block matrix that encodes interactions between both structures.

## Why It Matters
It lets us fuse two similarity spaces while preserving each matrix's internal geometry.

## Tiny Example
If `A` is `2x2` and `B` is `2x2`, then `A ⊗ B` is `4x4`, where each element of `A` scales a full copy of `B`.

## Definition
Given `A in R^{m x n}` and `B in R^{p x q}`,
\[
A \otimes B \in R^{mp \times nq}
\]
and each block is `a_ij * B`.

## Key Points
1. Dimensions multiply: `(m,n)` with `(p,q)` becomes `(mp,nq)`.
2. Determinant identity: `|A ⊗ B| = |A|^p |B|^m` (square case).
3. Useful for multi-view covariance/similarity fusion.

## How This Paper Uses It
- [[RBFleX-NAS]] defines score with `log|K ⊗ Q|`.
- Then simplifies it into `N(log|K| + log|Q|)` to reduce computation.

## Representative Papers
- [[RBFleX-NAS]]: Uses Kronecker fusion for dual similarity matrices.

## Related Concepts
- [[Radial Basis Function Kernel]]
- [[Hyperparameter Detection Algorithm]]
- [[Neural Architecture Search]]

