---
type: concept
aliases: [SSL, Self-Supervision]
---

# Self-Supervised Learning

## Intuition

Self-Supervised Learning (SSL) lets a model learn useful features from unlabeled data by creating supervision from the data itself.

## Why It Matters

SSL reduces dependence on expensive manual labels and often improves transfer to downstream tasks with limited annotations.

## Tiny Example

In masked image modeling, we hide image patches and ask the model to reconstruct them. The hidden patches act like pseudo-labels.

## Definition

SSL is a representation-learning paradigm where training targets are generated from intrinsic data structure (e.g., masking, prediction, contrastive matching) rather than external human labels.

## Key Points

1. SSL focuses on pretext tasks that create supervisory signals automatically.
2. The learned representations are usually adapted by fine-tuning on downstream tasks.
3. SSL is especially valuable in low-label or label-scarce domains.

## How This Paper Uses It

- [[GEN-TPC-NAS]]: Uses SSL as the training paradigm after search and designs Entropy proxy to estimate low-label generalization potential.

## Representative Papers

- [[MAE]]: Uses masked autoencoding for visual SSL.
- [[MaskTAS]]: Uses SSL in one-shot Transformer architecture search.

## Related Concepts

- [[Masked Image Modeling]]
- [[Zero-Cost Proxy]]

