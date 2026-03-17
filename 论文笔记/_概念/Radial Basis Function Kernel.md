---
type: concept
aliases: [RBF Kernel, Gaussian Kernel]
---

# Radial Basis Function Kernel

## Intuition
RBF kernel turns Euclidean distance into similarity. Close vectors get values near 1; far vectors get values near 0.

## Why It Matters
It captures non-linear relationships with a simple formula and is widely used for similarity modeling.

## Tiny Example
If two feature vectors differ only slightly, `exp(-gamma * ||x-y||^2)` stays high; if they differ a lot, the score quickly decays.

## Definition
For vectors `x_i, x_j`, RBF similarity is:
\[
K_{ij}=\exp(-\gamma \|x_i-x_j\|^2)
\]
where `gamma > 0` controls sensitivity.

## Key Points
1. `gamma` too large makes kernel values collapse toward 0 quickly.
2. `gamma` too small makes many pairs look similarly high.
3. Works well when relative distances carry semantic information.

## How This Paper Uses It
- [[RBFleX-NAS]] builds two RBF matrices:
  - one on activation outputs (`K`)
  - one on final-layer input features (`Q`)
- It then scores architecture quality from log-determinants of these matrices.

## Representative Papers
- [[RBFleX-NAS]]: Uses dual RBF kernels for training-free NAS scoring.
- Classic SVM literature: Uses RBF kernel for non-linear decision boundaries.

## Related Concepts
- [[Kronecker Product]]
- [[Hyperparameter Detection Algorithm]]
- [[Zero-Cost Proxy]]

