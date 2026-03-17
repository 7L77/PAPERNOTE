---
type: concept
aliases: [Momentum Iterative FGSM, MI-FGSM Attack]
---

# MI-FGSM

## Intuition

MI-FGSM adds momentum to iterative FGSM updates so perturbation steps are more stable and transferable.

## Why It Matters

It is a stronger attack than one-step FGSM and often transfers better across models.

## Tiny Example

At each step, gradient direction is accumulated with decay, then sign step is applied under epsilon budget.

## Definition

An iterative `l_inf` attack that normalizes gradients and accumulates momentum before perturbation update.

## Math Form (if needed)

Typical form:
`g_{t+1} = mu * g_t + grad_x L / ||grad_x L||_1`,
`x_{t+1} = clip_{x,eps}(x_t + alpha * sign(g_{t+1}))`.

## Key Points

1. Stronger than FGSM in many settings.
2. Momentum helps avoid poor local directions.
3. Common in robust-evaluation attack suites.

## How This Paper Uses It

- [[RNAS-CL]]: Reports MI-FGSM robustness in CIFAR-10 comparisons (Table 1).

## Representative Papers

- Dong et al. (2018): Introduces momentum iterative attack.

## Related Concepts

- [[FGSM]]
- [[PGD Attack]]
