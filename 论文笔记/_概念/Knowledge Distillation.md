---
type: concept
aliases: [KD, Teacher-Student Distillation]
---

# Knowledge Distillation

## Intuition

A smaller student model learns from a stronger teacher model, not only from hard labels.

## Why It Matters

It often improves compact model quality and stability, especially in lightweight NLP/CV settings.

## Tiny Example

A small model can match a large model's output logits and intermediate features to retain performance after compression.

## Definition

Knowledge distillation transfers knowledge from teacher to student through soft targets, feature alignment losses, or both.

## Math Form (if needed)

Common form:
`L = alpha * L_task + beta * L_distill`,
where `L_distill` may include logit KL/CE and hidden-state MSE losses.

## Key Points

1. Distillation can supervise outputs and intermediate representations.
2. It is widely used for model compression and NAS-selected compact models.
3. Loss weights and layer mapping strongly affect final quality.

## How This Paper Uses It

- [[W-PCA]]: Uses EfficientBERT-style KD losses for attention/hidden/embedding/prediction terms after search.

## Representative Papers

- EfficientBERT (Dong et al., 2021): Distillation-aware lightweight model search/training.

## Related Concepts

- [[Training-free NAS]]
- [[Neural Architecture Search]]
