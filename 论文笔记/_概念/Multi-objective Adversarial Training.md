---
type: concept
aliases: [Clean-Robust Joint Objective, Robustness-Accuracy Tradeoff Training]
---

# Multi-objective Adversarial Training

## Intuition
Instead of optimizing only clean accuracy or only robust accuracy, multi-objective adversarial training jointly optimizes both with a trade-off weight.

## Why It Matters
Robust NAS often needs to balance clean and robust performance. This objective makes the trade-off explicit and tunable.

## Tiny Example
If `beta=0`, training focuses only on clean samples. If `beta=1`, it focuses fully on adversarial samples. Intermediate `beta` values interpolate between the two goals.

## Definition
A common form is:
\[
\mathcal{L}(W)=(1-\beta)\mathcal{L}_{clean}(W)+\beta \mathcal{L}_{robust}(W), \quad \beta\in[0,1].
\]
`L_clean` measures standard prediction loss, while `L_robust` measures loss on adversarially perturbed inputs.

## Math Form (if needed)
\[
\mathcal{L}_{robust}(W)=\frac{1}{N}\sum_{i=1}^{N}\ell\big(y_i,f(A_{\epsilon}(x_i,W),W)\big)
\]

In [[NAS-RobBench-201]], this objective is also the anchor for the NTK-based generalization analysis.  
Source: [[NAS-RobBench-201]] Eq. (3), Sec. 4.1.

## Key Points
1. `beta` controls accuracy-robustness trade-off.
2. The training objective affects both benchmark ranking and theory kernels.
3. It can be viewed as a practical interface between empirical robust NAS and theory.

## How This Paper Uses It
- [[NAS-RobBench-201]]: defines benchmark training objective and derives clean/robust bounds from it.

## Representative Papers
- [[NAS-RobBench-201]]: uses this objective for both benchmark construction and generalization theory.
- [[AdvRush]]: robust NAS objective design with robustness-oriented regularization.

## Related Concepts
- [[Adversarial Robustness]]
- [[Robust Neural Tangent Kernel]]
- [[PGD Attack]]
- [[Robust Neural Architecture Search]]

