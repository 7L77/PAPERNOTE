---
type: concept
aliases: [NTK, Tangent Kernel]
---

# Neural Tangent Kernel

## Intuition
Neural Tangent Kernel (NTK) measures how similarly two inputs influence a network's parameters at a given point (often initialization). If two samples induce similar parameter gradients, they are "close" under NTK.

## Why It Matters
NTK gives a tractable way to analyze optimization and generalization behavior of neural networks, and is often used to derive training-loss bounds or architecture-quality surrogates.

## Tiny Example
Take two images `x1` and `x2`. If `∇θ f(x1)` and `∇θ f(x2)` point in similar directions, NTK between them is large, indicating updates for one sample may help the other.

## Definition
For model `fθ`, NTK between `x` and `x'` is the gradient inner product:
`Θθ(x, x') = <∇θ fθ(x), ∇θ fθ(x')>`.
In matrix form over a batch, eigenvalues of `Θ` are linked to optimization dynamics.

## Math Form (if needed)
$$
\Theta_{\theta}(x, x') = \left\langle \nabla_{\theta} f_{\theta}(x), \nabla_{\theta} f_{\theta}(x') \right\rangle
$$

Symbols:
- `fθ(x)`: model output for input `x`.
- `∇θ fθ(x)`: gradient of output w.r.t. parameters.
- `Θθ`: kernel matrix induced by parameter gradients.

## Key Points
1. NTK is gradient-geometry in parameter space.
2. Eigenvalues of NTK are frequently used in loss-bound analysis.
3. Initialization NTK is often used as a cheap proxy in training-free NAS.

## How This Paper Uses It
- [[Robust-ZCP]]: Uses an NTK-eigenvalue-related approximation term (Eq. 8) as one factor in the robustness proxy score.

## Representative Papers
- [[Robust-ZCP]]: Applies NTK-based approximation to adversarial robustness scoring.
- [[ZCP-Eval]]: Discusses zero-cost proxy behavior where gradient-based signals are central.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Input Loss Landscape]]
- [[Adversarial Robustness]]

