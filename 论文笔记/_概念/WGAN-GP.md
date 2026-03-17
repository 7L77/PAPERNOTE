---
type: concept
aliases: [Wasserstein GAN with Gradient Penalty, WGAN GP]
---

# WGAN-GP

## Intuition
WGAN-GP replaces unstable GAN divergence optimization with a Wasserstein-distance-inspired objective and enforces a smooth discriminator by penalizing gradient norm deviations from 1.

## Why It Matters
It improves adversarial training stability and gives more meaningful critic gradients, especially when vanilla GAN training is brittle.

## Tiny Example
When the discriminator gets too sharp, gradients to the generator may explode or vanish. WGAN-GP adds a penalty on interpolated samples to keep critic gradients near unit norm and stabilize updates.

## Definition
WGAN-GP optimizes:
`E[D(fake)] - E[D(real)] + lambda * E[(||∇_x_hat D(x_hat)||_2 - 1)^2]`,
where `x_hat` is an interpolation between real and generated samples.

## Key Points
1. Uses critic output without sigmoid as Wasserstein score surrogate.
2. Gradient penalty is usually applied on interpolated samples.
3. Often paired with multiple critic updates per generator update.

## How This Paper Uses It
- [[ZeroNAS]]: Uses WGAN-GP terms in both architecture-parameter and network-parameter updates for discriminator and generator search loops.

## Representative Papers
- [[ZeroNAS]]: Integrates WGAN-GP into differentiable GAN architecture search.

## Related Concepts
- [[Generative Adversarial Network]]
- [[Differentiable Architecture Search]]
- [[Zero-Shot Learning]]

