---
type: concept
aliases: ["Surrogate-free Search", "Predictorless Search"]
---

# Predictor-Free Search

## Intuition

Predictor-Free Search means searching architectures without training a separate accuracy predictor. Instead, it directly optimizes a cheap-to-compute proxy objective.

## Why It Matters

In many NAS pipelines, collecting subnet-accuracy pairs and training a surrogate predictor dominates runtime. Removing this stage can dramatically reduce search latency.

## Tiny Example

Instead of evaluating 10,000 subnets to train a regressor, we directly run GA on a structural fitness score and get a deployment candidate in seconds.

## Definition

Predictor-Free Search is a deployment-time NAS strategy where candidate architectures are ranked by directly computed objective signals (e.g., zero-cost or structural metrics), without fitting an explicit accuracy surrogate model.

## Key Points

1. It optimizes search speed and simplicity by removing predictor training.
2. Its success depends on proxy-quality rank correlation with true accuracy.
3. It often combines naturally with hard constraints (MACs, params, latency).

## How This Paper Uses It

- [[DeepFedNAS]]: uses unified fitness \(F(A)\) as a direct proxy and reports large pipeline speedup over predictor-based post-search.

## Representative Papers

- [[DeepFedNAS]]: predictor-free deployment search in federated NAS.
- [[Zero-Cost Proxy]]: broader family of cheap proxy signals used for fast architecture ranking.

## Related Concepts

- [[Genetic Algorithm]]
- [[Zero-Cost Proxy]]
- [[Hardware-aware NAS]]

