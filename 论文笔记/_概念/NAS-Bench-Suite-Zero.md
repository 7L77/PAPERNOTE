---
type: concept
aliases: [NASBenchSuiteZero, NB-Suite-Zero]
---

# NAS-Bench-Suite-Zero

## Intuition
NAS-Bench-Suite-Zero is a benchmark resource that provides training-free proxy scores for architectures across multiple NAS search spaces.

## Why It Matters
It enables fast, reproducible studies of zero-cost proxies without recomputing each metric from scratch.

## Tiny Example
Instead of running SynFlow for every architecture manually, you query precomputed SynFlow values from the benchmark.

## Definition
A tabular benchmark suite that aggregates zero-cost metric values for many architectures and search spaces, designed to accelerate proxy-based NAS research.

## Key Points
1. Focuses on training-free proxy metadata.
2. Useful for objective-function comparisons in NAS.
3. Reduces compute and improves reproducibility.

## How This Paper Uses It
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Queries SynFlow scores for candidate architectures during search setup.

## Representative Papers
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Uses it together with NAS-RobBench-201 for robust objective evaluation.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]

