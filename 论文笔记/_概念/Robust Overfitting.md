---
type: concept
aliases: [RO, Adversarial Robust Overfitting]
---

# Robust Overfitting

## Intuition
Robust Overfitting means that during adversarial training, test-time robustness can start degrading after a point even though training robustness keeps improving.

## Why It Matters
It is a major failure mode in adversarial training and directly affects model selection, checkpoint policy, and fair comparison of robust architectures.

## Tiny Example
A model's validation PGD accuracy peaks at epoch 70 but drops by epoch 100, while training adversarial accuracy keeps rising. Picking the last epoch would overestimate training quality but underestimate real robustness.

## Definition
A phenomenon where prolonged adversarial training leads to reduced out-of-sample adversarial robustness, typically observed as a gap between training and validation/test robust accuracy trajectories.

## Math Form (if needed)
No single canonical formula; it is typically diagnosed from robustness curves over training epochs.

## Key Points
1. It is common in standard adversarial training with fixed schedules.
2. Early stopping on robust validation metrics is a practical mitigation.
3. Ignoring it can bias conclusions about architecture quality.

## How This Paper Uses It
- [[NARes]]: Uses a separate validation set and best-PGD-CW40 checkpoint selection to mitigate robust overfitting when building the dataset.

## Representative Papers
- Rice et al. (2020): Formalizes and studies robust overfitting behavior in adversarial training.
- [[NARes]]: Applies mitigation in a large-scale architecture dataset pipeline.

## Related Concepts
- [[Adversarial Training]]
- [[Adversarial Robustness]]
- [[PGD Attack]]
