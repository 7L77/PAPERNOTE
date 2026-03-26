---
type: concept
aliases: [Adversarial Space, Perturbed Input Space]
---

# Adversarial Input Space

## Intuition

Adversarial input space is the set of perturbed samples used to evaluate model behavior under attack-like conditions instead of only clean inputs.

## Why It Matters

If robust NAS scoring is done only on clean data, it may miss robustness-relevant structure preferences. Evaluating in adversarial space can align search with robustness goals earlier.

## Tiny Example

Given clean set \(\{(x_i,y_i)\}\), add perturbation to obtain \(\{(x_i+\delta_i,y_i)\}\) or \(\{(x_i+v,y_i)\}\). The latter is a UAP-based adversarial input space.

## Definition

A constructed set \(D_A\) where each clean sample is replaced by an adversarially perturbed counterpart under a perturbation constraint.

## Key Points

1. Construction method matters: per-sample attacks vs universal perturbation can lead to different transfer properties.
2. A transferable adversarial space is critical for comparing many architectures fairly.
3. Strong attack space can improve robustness-oriented ranking but may increase construction complexity.

## How This Paper Uses It

- [[RTP-NAS]]: defines \(D_A=\{(x_i+v,y_i)\}\) with UAP and computes pruning indicators in this space.

## Representative Papers

- [[RTP-NAS]]: uses UAP-based adversarial space for training-free robust NAS.

## Related Concepts

- [[Universal Adversarial Perturbation]]
- [[Adversarial Robustness]]
- [[FGSM]]
- [[PGD Attack]]
