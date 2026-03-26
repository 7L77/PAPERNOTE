---
type: concept
aliases: [UAP, Universal Perturbation]
---

# Universal Adversarial Perturbation

## Intuition

A Universal Adversarial Perturbation (UAP) is one shared noise pattern that can fool a model on many different images, instead of crafting a separate perturbation for each image.

## Why It Matters

UAP can build a reusable adversarial test space cheaply. In robust NAS, this helps compare many candidate architectures without repeatedly generating per-sample attacks.

## Tiny Example

Instead of creating 10,000 different PGD perturbations for 10,000 images, you learn one perturbation \(v\), then test all images with \(x_i+v\).

## Definition

Given dataset \(D_S=\{(x_i,y_i)\}\), UAP seeks a single \(v\) such that:

\[
\mathcal{C}(x_i+v)\neq y_i,\quad \|v\|_p\le\epsilon
\]

for most samples \(x_i\in D_S\).

## Key Points

1. UAP is sample-agnostic and shared across inputs.
2. Transferability across architectures is the key practical value.
3. A high fooling ratio alone does not guarantee best transfer for robust NAS scoring.

## How This Paper Uses It

- [[RTP-NAS]]: uses UAP to construct [[Adversarial Input Space]] for architecture pruning scores.

## Representative Papers

- [[RTP-NAS]]: robust training-free NAS with UAP-based scoring space.
- [[Adversarial Robustness]]: broad robustness context where universal perturbations are studied.

## Related Concepts

- [[Adversarial Input Space]]
- [[FGSM]]
- [[PGD Attack]]
- [[Adversarial Robustness]]
