---
type: concept
aliases: [Performance Predictor, Surrogate Model]
---

# Surrogate Predictor

## Intuition
A surrogate predictor is a fast model that estimates architecture performance without full training.

## Why It Matters
Full NAS evaluation is expensive. A good surrogate filters weak candidates early and saves compute.

## Tiny Example
Encode an architecture graph into a vector, feed it to an MLP predictor, and use predicted accuracy to rank candidates.

## Definition
In NAS, a surrogate predictor is an auxiliary regression/classification model trained to approximate the fitness (e.g., validation accuracy) of candidate architectures.

## Key Points
1. Reduces expensive full evaluations.
2. Needs frequent calibration to avoid ranking drift.
3. Works best when architecture encoding captures structural semantics.

## How This Paper Uses It
- [[LLMENAS]]: Uses predictor score `s=g_phi(E(P))` for fast candidate scoring inside the LLM-guided evolutionary loop.

## Representative Papers
- [[NAS-Bench-101]]: Benchmark setting enabling predictor studies.
- [[BANANAS]]: Bayesian optimization with neural predictors.

## Related Concepts
- [[One-shot NAS]]
- [[Neural Architecture Search]]
- [[LLM-guided Search]]

