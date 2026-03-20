---
type: concept
aliases: [FID, Fréchet Inception Distance]
---

# Frechet Inception Distance

## Intuition

FID measures whether generated images look like they came from the same distribution as real images. It is not judging one image at a time; it compares the overall cloud of generated features against the cloud of real features.

## Why It Matters

A GAN can generate some sharp images yet still have poor coverage or unstable diversity. FID is useful because it penalizes both unrealistic samples and distribution mismatch.

## Tiny Example

If a generator makes only very clean cat images while the real dataset contains cats, dogs, and trucks, image quality may look good locally but the generated feature cloud will still sit far from the real one, so FID stays high.

## Definition

FID computes the Fréchet distance between two multivariate Gaussian approximations in the feature space of an Inception network: one for real samples and one for generated samples.

## Math Form (if needed)

For real-feature mean/covariance `(μ_r, Σ_r)` and generated-feature mean/covariance `(μ_g, Σ_g)`,

$$
\mathrm{FID} =
\|\mu_r - \mu_g\|_2^2 +
\mathrm{Tr}(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2})
$$

where `μ` captures feature-center mismatch and `Σ` captures feature-spread mismatch. Lower is better.

## Key Points

1. FID is a distribution-level metric, not a per-sample realism score.
2. Lower FID means generated samples are closer to the real data distribution in feature space.
3. FID is often more informative than IS when diversity or mode coverage matters.

## How This Paper Uses It

- [[EAS-GAN]]: Uses FID as the main quantitative metric on CIFAR-10, STL-10, and LSUN bedroom, and reports the strongest gains through lower values.

## Representative Papers

- [[EAS-GAN]]: Shows how a searched GAN architecture can improve FID over fixed-architecture and RL-based GAN baselines.

## Related Concepts

- [[Inception Score]]
- [[Generative Adversarial Network]]
- [[Mode Collapse]]

