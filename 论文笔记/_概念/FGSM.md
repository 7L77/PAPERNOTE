---
type: concept
aliases: [Fast Gradient Sign Method, One-step Attack]
---

# FGSM

## Intuition
FGSM perturbs each input pixel in the sign direction of the loss gradient to increase model error in one step.

## Why It Matters
It is a cheap and widely used baseline attack/training tool in adversarial robustness research.

## Tiny Example
If a pixel's gradient is positive, FGSM adds `+eps`; if negative, it adds `-eps`.

## Definition
Given input `x`, label `y`, and loss `L`, FGSM attack is:
\[
x_{adv} = x + \epsilon \cdot \mathrm{sign}(\nabla_x L(f_\theta(x), y)).
\]

## Math Form (if needed)
`eps` controls perturbation budget under `l_inf` norm.

## Key Points
1. Single-step and fast.
2. Weaker than multi-step attacks like PGD but useful for fast training.
3. Can be strengthened with random initialization.

## How This Paper Uses It
- [[ABanditNAS]]: Uses FGSM with random initialization during search/training to reduce adversarial optimization cost.

## Representative Papers
- Goodfellow et al., "Explaining and Harnessing Adversarial Examples" (2014).
- Wong et al., "Fast is Better than Free" (2020).

## Related Concepts
- [[PGD Attack]]
- [[Adversarial Robustness]]
- [[ABanditNAS]]

