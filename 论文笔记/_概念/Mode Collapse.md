---
type: concept
aliases: [GAN Mode Collapse]
---

# Mode Collapse

## Intuition

Mode collapse means a generator keeps producing only a narrow slice of the true data distribution, even if those samples individually look plausible.

## Why It Matters

This is one of the classic GAN failure modes. A model that collapses may seem visually decent on a few outputs but fails to represent the diversity the task actually needs.

## Tiny Example

Suppose a dataset contains many room layouts, but the generator repeatedly outputs only one or two bedroom styles. The images may look realistic, yet the generator has collapsed to a few modes.

## Definition

Mode collapse is the failure of a generative model, especially a GAN, to cover multiple modes of the target distribution, often due to unstable adversarial dynamics or weak training signals for diversity.

## Key Points

1. Good-looking samples do not rule out collapse.
2. Collapse is about distribution coverage, not only sample sharpness.
3. Loss design, discriminator behavior, and architecture choices all affect collapse risk.

## How This Paper Uses It

- [[EAS-GAN]]: Motivates multiple mutation objectives and diversity-aware fitness partly to reduce the risk of mode collapse during evolutionary GAN training.

## Representative Papers

- [[EAS-GAN]]: Frames mutation diversity and selection as practical tools to avoid collapse while improving generator search.

## Related Concepts

- [[Generative Adversarial Network]]
- [[Frechet Inception Distance]]
- [[Inception Score]]

