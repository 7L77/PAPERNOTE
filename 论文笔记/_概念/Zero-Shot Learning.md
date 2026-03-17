---
type: concept
aliases: [ZSL, Zero Shot Learning]
---

# Zero-Shot Learning

## Intuition
Zero-Shot Learning asks a model to recognize classes that never appear in training images by transferring knowledge through side information, usually semantic attributes or text embeddings.

## Why It Matters
Collecting labeled data for every possible class is expensive or impossible. ZSL offers a way to scale recognition to unseen categories without collecting new annotated images for each class.

## Tiny Example
Suppose training only contains seen animals such as horse and zebra, but test contains "okapi." If the model knows semantic attributes of okapi (striped, hoofed, herbivore), it can map test features to that unseen label.

## Definition
Given disjoint seen label set `Y_s` and unseen label set `Y_u`, ZSL trains on seen classes only and predicts labels from unseen classes at test time using a shared semantic space.

## Key Points
1. Seen and unseen label sets are disjoint during training.
2. Semantic representations are the bridge between seen and unseen classes.
3. Generative ZSL synthesizes unseen features first, then trains a standard classifier.

## How This Paper Uses It
- [[ZeroNAS]]: Uses GAN-generated unseen features and searches GAN architecture to improve ZSL accuracy.

## Representative Papers
- [[ZeroNAS]]: Introduces differentiable joint GAN architecture search for ZSL.

## Related Concepts
- [[Generalized Zero-Shot Learning]]
- [[Generative Adversarial Network]]
- [[Neural Architecture Search]]

