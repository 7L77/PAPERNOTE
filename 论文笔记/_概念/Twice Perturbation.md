---
type: concept
aliases: [Double Adversarial Perturbation, Two-step Perturbed Input]
---

# Twice Perturbation

## Intuition
Twice perturbation means attacking an already attacked sample again, instead of simply increasing the step size in one attack run.

## Why It Matters
It builds a stronger adversarial view that can reveal robustness differences missed by milder perturbations, and is used in this paper's robust NTK theory.

## Tiny Example
Given image `x`, first generate `x_adv1 = A_eps(x)`. Then run attack again on `x_adv1` to get `x_adv2 = A_eps(x_adv1)`. The second sample is generally not equivalent to one-shot larger-step PGD on `x`.

## Definition
Let `A_eps` be an adversary with radius `eps`. Twice perturbation defines:
- first perturbation: `x_adv = A_eps(x)`
- second perturbation: `x_adv2 = A_eps(x_adv)`

In the paper, kernels built from `x_adv2` appear in robust bound terms for stronger perturbation analysis.

## Math Form (if needed)
\[
\hat{x} = A_{\epsilon}(A_{\epsilon}(x))
\]

This is conceptually different from "single perturbation with doubled step size".  
Source: [[NAS-RobBench-201]] Sec. 4.2 discussion after Eq. (5).

## Key Points
1. Two attacks in sequence are not equal to one attack with larger step.
2. It can produce stronger adversarial samples in analysis.
3. The paper uses it to define robust-twice NTK components.

## How This Paper Uses It
- [[NAS-RobBench-201]]: introduces twice-perturbation kernels in `\tilde{K}_{all}` for robust generalization analysis.

## Representative Papers
- [[NAS-RobBench-201]]: explicit robust-twice kernel construction.
- de Jorge et al. (2022): cited as motivation related to catastrophic overfitting discussion.

## Related Concepts
- [[Robust Neural Tangent Kernel]]
- [[PGD Attack]]
- [[Adversarial Robustness]]
- [[Multi-objective Adversarial Training]]

