---
type: concept
aliases: [AT, Robust Training]
---

# Adversarial Training

## Intuition
Adversarial training makes the model learn from hard perturbed examples during training, so attacks at test time are less surprising.

## Why It Matters
It is one of the most effective general strategies for improving adversarial robustness in classification.

## Tiny Example
Each training step mixes clean and PGD/FGSM-perturbed samples, forcing the model to classify both correctly.

## Definition
Adversarial training is robust optimization that minimizes worst-case loss over perturbation sets, typically approximated by inner-loop attacks.

## Key Points
1. Usually improves robustness but may reduce clean accuracy.
2. Attack choice during training strongly affects generalization to unseen attacks.
3. Computational cost is much higher than standard training.

## How This Paper Uses It
- [[Padding-Robustness Interplay]]: Compares native vs FGSM-based adversarially trained models and shows padding rankings change under AT.

## Representative Papers
- [[Towards Deep Learning Models Resistant to Adversarial Attacks]]: Canonical robust optimization formulation.

## Related Concepts
- [[Adversarial Robustness]]
- [[APGD-CE]]

