---
type: concept
aliases: [Jacobian, Jacobian Matrix of Network Output]
---

# Jacobian Matrix

## Intuition
The Jacobian matrix describes how each output changes with small changes in parameters or inputs.

## Why It Matters
It captures local sensitivity and geometry; many training-free NAS proxies use Jacobian-derived statistics.

## Tiny Example
If one output logit changes a lot when a parameter changes slightly, the corresponding Jacobian entry is large.

## Definition
For vector function `f`, Jacobian is `J_ij = partial f_i / partial x_j` (or w.r.t. parameters `w`).

## Math Form (if needed)
For a batch `{x_b}` and model parameters `w`:
`J = [partial f(x_1)/partial w; ...; partial f(x_B)/partial w]`.

## Key Points
1. Encodes local gradient structure.
2. Singular values/eigenvalues of Jacobian-related matrices are informative.
3. Often used to build zero-cost expressivity proxies.

## How This Paper Uses It
- [[IBFS]]: Computes Jacobian at initialization and scores architectures by entropy over Jacobian spectra.

## Representative Papers
- [[IBFS]]: Uses Jacobian spectrum entropy for ranking.
- [[NASWOT]]: Uses Jacobian-based binary-code distance proxy.

## Related Concepts
- [[Neural Tangent Kernel]]
- [[Entropy]]
- [[Zero-Cost Proxy]]
