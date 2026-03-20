---
type: concept
aliases: [IS]
---

# Inception Score

## Intuition

Inception Score asks two things at once: does each generated image look confidently classifiable, and are the generated images varied across classes?

## Why It Matters

It was an early popular GAN metric because it tries to reward both image quality and class diversity using a pretrained classifier.

## Tiny Example

If every generated image is confidently classified as "dog," the first part looks good but the second part fails because the class distribution is too narrow. IS therefore drops.

## Definition

IS measures the KL divergence between the conditional label distribution `p(y|x)` and the marginal label distribution `p(y)` over generated samples. High confidence per image and broad coverage across labels raise the score.

## Math Form (if needed)

$$
\exp\left(\mathbb{E}_{x} \left[ D_{KL}(p(y|x)\|p(y)) \right]\right)
$$

where `p(y|x)` comes from a pretrained Inception classifier. Higher is better.

## Key Points

1. IS rewards confidence and diversity, but only through classifier labels.
2. It does not directly compare generated images with real images.
3. IS can be misleading when the classifier or dataset mismatch is large.

## How This Paper Uses It

- [[EAS-GAN]]: Reports IS on CIFAR-10 and STL-10, but explicitly argues that FID is the fairer and more comprehensive metric.

## Representative Papers

- [[EAS-GAN]]: Uses IS as a secondary metric and criticizes reward designs that optimize directly for IS.

## Related Concepts

- [[Frechet Inception Distance]]
- [[Generative Adversarial Network]]
- [[Mode Collapse]]

