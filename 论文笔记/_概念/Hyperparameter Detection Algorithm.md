---
type: concept
aliases: [HDA]
---

# Hyperparameter Detection Algorithm

## Intuition
HDA estimates kernel hyperparameters from feature statistics instead of manual tuning.

## Why It Matters
Kernel methods are highly sensitive to `gamma`. Poor values can destroy similarity contrast.

## Tiny Example
If two sample groups have large mean gap but tiny variance, HDA returns a larger candidate gamma than cases with noisy overlap.

## Definition
For vector pair `(v_i, v_j)`, define:
- mean gap term `D_ij = (m_i - m_j)^2`
- variance terms `s_i^2, s_j^2`
- candidate `G_ij = D_ij / (2(s_i^2 + s_j^2))`
Then select a robust final gamma from candidate matrix entries.

## Key Points
1. Uses both separation (`D_ij`) and spread (`s_i^2 + s_j^2`).
2. Avoids expensive grid search.
3. Can be run on a small subset of sampled networks.

## How This Paper Uses It
- [[RBFleX-NAS]] computes `G_k` for activation outputs and `G_q` for last-layer inputs.
- Final `gamma_k`, `gamma_q` are chosen by taking minimum valid entries.

## Representative Papers
- [[RBFleX-NAS]]: Introduces HDA for dual RBF kernels in NAS scoring.

## Related Concepts
- [[Radial Basis Function Kernel]]
- [[Fisher Linear Discriminant]]
- [[Zero-Cost Proxy]]

