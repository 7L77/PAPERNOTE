---
type: concept
aliases: [GAN, Generative Adversarial Networks]
---

# Generative Adversarial Network

## Intuition
A GAN trains two models in competition: a generator tries to produce realistic samples, and a discriminator tries to distinguish real from generated ones.

## Why It Matters
The adversarial game can learn rich data distributions without explicit density formulas, making GANs effective for synthesis, augmentation, and representation learning.

## Tiny Example
If the generator outputs synthetic visual features for unseen classes and the discriminator cannot tell them from real seen features, those synthetic features become useful for downstream classification.

## Definition
A GAN is a minimax learning framework:
`min_G max_D V(D,G)`, where `D` scores real/fake and `G` maps noise (optionally conditioned inputs) to synthetic samples.

## Key Points
1. Generator and discriminator are coupled; stability depends on both.
2. Training dynamics are sensitive to losses, regularization, and architecture.
3. Conditional GANs inject side information (e.g., class attributes) into both G and D.

## How This Paper Uses It
- [[ZeroNAS]]: Searches both generator and discriminator architectures jointly for conditional feature synthesis in ZSL.

## Representative Papers
- [[ZeroNAS]]: Uses differentiable NAS to optimize GAN architecture pair (G, D).

## Related Concepts
- [[WGAN-GP]]
- [[Zero-Shot Learning]]
- [[Differentiable Architecture Search]]

