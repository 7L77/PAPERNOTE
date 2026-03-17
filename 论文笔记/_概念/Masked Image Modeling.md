---
type: concept
aliases: [MIM, Masked Modeling]
---

# Masked Image Modeling

## Intuition

Masked Image Modeling trains a model to recover missing image content, so the model must learn semantic structure rather than memorizing labels.

## Why It Matters

It is a strong SSL pretext task for Vision Transformers and provides representations that transfer well with limited labels.

## Tiny Example

Split an image into patches, randomly mask 75%, and reconstruct masked pixels from visible patches.

## Definition

MIM is an SSL objective where image tokens/patches are partially masked, and the model is optimized to predict missing information (pixels, features, or tokens).

## Key Points

1. Mask ratio controls difficulty and representation pressure.
2. MIM is typically pre-training only; downstream tasks use fine-tuning.
3. Good MIM pretraining often improves low-label performance.

## How This Paper Uses It

- [[GEN-TPC-NAS]]: Uses MIM-style SSL pre-training to evaluate searched ViT architectures under low-label fine-tuning.

## Representative Papers

- [[MAE]]: Canonical masked autoencoder framework.
- [[MaskTAS]]: SSL Transformer architecture search with masking and distillation.

## Related Concepts

- [[Self-Supervised Learning]]
- [[Zero-Cost Proxy]]
