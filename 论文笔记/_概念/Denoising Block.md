---
type: concept
aliases: [Feature Denoising Block, Non-local Denoising]
---

# Denoising Block

## Intuition
A denoising block suppresses noisy or adversarially perturbed feature responses and keeps more stable semantic structure.

## Why It Matters
Adversarial perturbations often amplify harmful high-frequency or non-robust features; denoising modules can improve robustness.

## Tiny Example
Given a feature map, a non-local denoising block computes weighted averages across spatial positions so outlier responses are smoothed.

## Definition
A denoising block applies a denoising operator (e.g., non-local mean) to feature maps, often wrapped with projection layers and residual connections.

## Math Form (if needed)
One form is:
\[
z_p = \frac{1}{C(x)}\sum_{q \in L} f(x_p, x_q)\,x_q,
\]
where `f` is a similarity weighting function and `C(x)` is normalization.

## Key Points
1. Works in feature space, not only input space.
2. Can improve adversarial robustness but adds compute.
3. Placement in early/intermediate layers changes effect.

## How This Paper Uses It
- [[ABanditNAS]]: Includes denoising block as a searchable primitive to improve model defense.

## Representative Papers
- Buades et al., non-local means denoising (2005).
- Xie et al., feature denoising for adversarial robustness (CVPR 2019).

## Related Concepts
- [[Gabor Filter]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]

