---
type: concept
aliases: ["Pareto Path Curriculum", "Pareto Cache Guided Training"]
---

# Pareto-Guided Supernet Training

## Intuition

Instead of sampling random subnets during supernet training, we first build a Pareto-quality subnet cache and train mostly on these better candidates.

## Why It Matters

Random sampling in huge search spaces often updates shared weights with low-quality architectures, which can hurt supernet conditioning and later search quality.

## Tiny Example

If a 60-subnet cache spans good architectures from low to high MACs, training clients on this cache gives cleaner gradients than repeatedly sampling weak random subnets.

## Definition

Pareto-Guided Supernet Training is a curriculum strategy that uses a pre-computed Pareto-optimal (or near-optimal) architecture set to guide subnet assignment during weight-sharing supernet optimization.

## Key Points

1. It turns subnet sampling from unguided random exploration into structured curriculum learning.
2. It improves shared-weight quality for post-training architecture extraction.
3. It can preserve budget coverage by caching candidates across multiple resource targets.

## How This Paper Uses It

- [[DeepFedNAS]]: generates a 60-subnet Pareto cache and uses boundary-plus-cache sampling in federated rounds.

## Representative Papers

- [[DeepFedNAS]]: formalized federated Pareto-guided training with predictor-free search.
- [[SuperFedNAS]]: baseline framework that this idea improves over by replacing random sampling.

## Related Concepts

- [[Pareto Front]]
- [[Super-network]]
- [[Federated Neural Architecture Search]]

