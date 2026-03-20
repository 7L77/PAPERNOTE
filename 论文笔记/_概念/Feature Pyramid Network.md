---
type: concept
aliases: [FPN, Feature Pyramid]
---

# Feature Pyramid Network

## Intuition

A Feature Pyramid Network combines features from multiple spatial scales so a detector can reason about small and large objects at the same time. This creates multiple branches and shared feature pathways, which makes pruning structurally tricky.

## Why It Matters

Many detection models are built on FPN-like necks. If pruning ignores these cross-scale connections, it may fail to convert theoretical compression into real detector speedup.

## Tiny Example

A detector may combine high-resolution shallow features with low-resolution deep features to build pyramid levels `P3` to `P7`. Removing channels from one branch affects lateral and top-down paths together.

## Definition

Feature Pyramid Network is a multi-scale feature aggregation architecture that builds semantically strong representations at several resolutions by combining bottom-up, lateral, and top-down pathways.

## Key Points

1. It is a standard neck design in object detection.
2. It creates cross-branch structural coupling.
3. Efficient pruning must account for both backbone and pyramid/head interactions.

## How This Paper Uses It

- [[Group Fisher Pruning]]: Uses layer grouping to handle coupled channels across FPN and detection heads, enabling structured pruning for RetinaNet, FSAF, ATSS, PAA, and Faster R-CNN settings discussed in the paper.

## Representative Papers

- [[Group Fisher Pruning]]: Extends structured pruning from simple backbones to FPN-based detectors.

## Related Concepts

- [[Coupled Channels]]
- [[Channel Pruning]]
- [[Group Convolution]]
