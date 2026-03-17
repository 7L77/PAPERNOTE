---
type: concept
aliases: [Robust NTK, Adversarial NTK]
---

# Robust Neural Tangent Kernel

## Intuition
Robust NTK extends the NTK view from clean inputs to adversarially perturbed inputs, so we can reason about robustness-aware learning dynamics instead of only standard generalization.

## Why It Matters
For robust NAS, clean-only signals can mis-rank architectures. Robust NTK provides a proxy signal that better matches adversarially trained performance.

## Tiny Example
Suppose two architectures have similar clean NTK scores. Under adversarial perturbation, architecture A keeps a stronger robust NTK score than B. In robust benchmark rankings, A is typically more competitive.

## Definition
Given adversary `A_eps`, robust NTK uses perturbed samples in kernel construction, e.g.:
- clean kernel: `K(i,j) = k(x_i, x_j)`
- robust kernel: `K_tilde_eps(i,j) = k(A_eps(x_i), A_eps(x_j))`
- cross kernel terms between clean and perturbed inputs may also be included.

In this paper, mixed kernels for clean/robust bounds combine clean, cross, and robust terms with weight `beta`.

## Math Form (if needed)
\[
K_{all} = (1-\beta)^2 K + \beta(1-\beta)(\bar{K}_{\epsilon} + \bar{K}_{\epsilon}^{\top}) + \beta^2 \tilde{K}_{\epsilon}
\]

\[
\tilde{K}_{all} = (1-\beta)^2 \tilde{K}_{\epsilon} + \beta(1-\beta)(\bar{K}_{2\epsilon} + \bar{K}_{2\epsilon}^{\top}) + \beta^2 \tilde{K}_{2\epsilon}
\]

`beta` is the clean/robust trade-off coefficient.  
Source: [[NAS-RobBench-201]] Eq. (4)-(5).

## Key Points
1. Robust NTK is a robustness-aware extension of NTK, not just a clean-kernel re-labeling.
2. It can correlate better with robust accuracy than clean NTK under adversarial training.
3. Twice-perturbation variants can strengthen correlation in stronger threat regimes.

## How This Paper Uses It
- [[NAS-RobBench-201]]: Defines mixed kernels and links minimum-eigenvalue-related quantities to clean/robust generalization bounds.

## Representative Papers
- [[NAS-RobBench-201]]: formalizes robust/mixed NTK in multi-objective adversarial training analysis.
- [[TRNAS]]: uses NTK-style signals for robust architecture search in practice.

## Related Concepts
- [[Neural Tangent Kernel]]
- [[Twice Perturbation]]
- [[Multi-objective Adversarial Training]]
- [[Adversarial Robustness]]

