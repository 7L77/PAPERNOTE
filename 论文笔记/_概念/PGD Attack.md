---
type: concept
aliases: [Projected Gradient Descent Attack, PGD]
---

# PGD Attack

## Intuition
PGD repeatedly takes small gradient-ascent steps on input and projects back to the allowed perturbation set.

## Why It Matters
It is a strong first-order adversary and a standard benchmark for adversarial robustness.

## Tiny Example
Starting from a random perturbation within `l_inf` ball, update 7 or 20 steps; after each step, clip back to `[-eps, eps]` around original input.

## Definition
A typical `l_inf` PGD update:
\[
x_{t+1} = \Pi_{B_\epsilon(x)}\big(x_t + \alpha \cdot \mathrm{sign}(\nabla_x L(f_\theta(x_t), y))\big),
\]
where `Pi` denotes projection to the `eps`-ball around clean input `x`.

## Math Form (if needed)
More steps usually yield stronger attacks but higher computational cost.

## Key Points
1. Multi-step extension of FGSM.
2. Commonly used for robustness evaluation (e.g., PGD-7/20/40/100).
3. Often paired with random restart for stronger attacks.

## How This Paper Uses It
- [[ABanditNAS]]: Reports robustness under PGD attacks (PGD-7/20 for CIFAR-10, PGD-40/100 for MNIST evaluations).

## Representative Papers
- Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks" (2017).
- Kurakin et al., "Adversarial examples in the physical world" (2016).

## Related Concepts
- [[FGSM]]
- [[Adversarial Robustness]]
- [[ABanditNAS]]

