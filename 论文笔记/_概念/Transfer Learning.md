---
type: concept
aliases: [Knowledge Transfer, Fine-tuning]
---

# Transfer Learning

## Intuition
Transfer Learning reuses knowledge learned on one task/domain to speed up or improve learning on another related task/domain.

## Why It Matters
Training from scratch is expensive. Reusing pretrained parameters often improves sample efficiency and final performance, especially with limited target data/compute.

## Tiny Example
A vision model pretrained on ImageNet is fine-tuned for medical image classification with much less data than a scratch model would need.

## Definition
Given a source task `Ts` and target task `Tt`, transfer learning initializes part or all of the target model using source-trained parameters, then adapts to `Tt`.

## Math Form (if needed)
A common form is parameter initialization:
`theta_t(0) <- theta_s*`
then optimize on target objective:
`theta_t* = argmin_theta L_t(theta)`.

## Key Points
1. Positive transfer improves target performance or efficiency.
2. Negative transfer hurts target performance when source-target mismatch is large.
3. Fine-tuning depth and learning-rate schedule are key controls.

## How This Paper Uses It
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: transfers RL-NAS agent parameters from one TransNAS-Bench-101 task to another (zero-shot / fine-tune / re-train).

## Representative Papers
- Pan and Yang, 2010: transfer learning survey.
- Yosinski et al., 2014: transferability of deep features.

## Related Concepts
- [[Reinforcement Learning]]
- [[Neural Architecture Search]]

