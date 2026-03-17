---
type: concept
aliases: [Surrogate Benchmark for NAS, Learned NAS Benchmark]
---

# Surrogate NAS Benchmark

## Intuition

A surrogate NAS benchmark replaces expensive architecture training with a learned predictor, so benchmarking can run fast while still approximating the behavior of the real search space.

## Why It Matters

Tabular NAS benchmarks need exhaustive evaluation and therefore small search spaces. Surrogate benchmarks scale to realistic spaces where exhaustive lookup is impossible.

## Tiny Example

Instead of training every candidate for 1-2 hours, you query a fitted model that returns predicted validation performance in less than a second, then compare optimizers by their anytime trajectories.

## Definition

A surrogate NAS benchmark is a benchmarking system where architecture performance (and often runtime) is estimated by trained surrogate models over a defined search space, rather than by exact table lookup or full retraining per query.

## Key Points

1. It trades exactness for scalability and repeatability.
2. Quality depends on data coverage and surrogate generalization.
3. It should be used as a black-box benchmark to avoid optimizer overfitting to surrogate internals.

## How This Paper Uses It

- [[NAS-Bench-301]]: Constructs a surrogate benchmark for the DARTS search space (>10^18 architectures) and validates ranking/trajectory fidelity against real evaluations.

## Representative Papers

- [[NAS-Bench-301]]: Canonical benchmark-focused surrogate construction.
- [[Surrogate Predictor]]: Broader predictor concept that surrogate benchmarks build upon.

## Related Concepts

- [[Surrogate Predictor]]
- [[Neural Architecture Search]]
- [[Sparse Kendall Tau]]

