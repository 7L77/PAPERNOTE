---
type: concept
aliases: [Input Landscape, Loss Landscape over Inputs]
---

# Input Loss Landscape

## Intuition
Input loss landscape describes how the loss changes when we slightly perturb the input while keeping model parameters fixed. A steep or highly curved landscape around a sample usually implies higher adversarial sensitivity.

## Why It Matters
Adversarial robustness is fundamentally about local behavior around input points. If tiny perturbations can sharply increase loss, the model is fragile under attacks.

## Tiny Example
If adding a tiny signed perturbation to an image causes cross-entropy to jump a lot, the local input landscape is sharp; if loss changes slowly, the landscape is smoother and usually more robust.

## Definition
Given fixed parameters `θ`, input landscape studies local properties of `L(θ, x)` in `x`-space, including gradient norm and Hessian curvature. Robustness-oriented methods often use these local quantities as surrogates.

## Math Form (if needed)
One practical curvature proxy is finite-difference on input gradients:
$$
\left\|
\frac{l(x + h z^*) - l(x)}{h}
\right\|_2^2,\quad l(x)=\nabla_x L(\theta, x)
$$

Symbols:
- `L(θ, x)`: loss at input `x`.
- `l(x)`: input gradient of loss.
- `h`: perturbation scale.
- `z*`: chosen perturbation direction (often sign-gradient direction).

## Key Points
1. It focuses on local geometry in input space, not parameter space.
2. High local curvature often correlates with adversarial vulnerability.
3. Finite-difference approximations can estimate curvature cheaply.

## How This Paper Uses It
- [[Robust-ZCP]]: Uses the finite-difference term (Eq. 7) as an approximation to the input-Hessian-related adversarial-loss upper-bound component.

## Representative Papers
- [[Robust-ZCP]]: Combines input-landscape term with NTK term for zero-cost robust ranking.
- [[Adversarial Robustness]]: Broad line of work relating local loss geometry to attack success.

## Related Concepts
- [[Neural Tangent Kernel]]
- [[Adversarial Robustness]]
- [[Zero-Cost Proxy]]

