---
type: concept
aliases: [TransNAS101]
---

# TransNAS-Bench-101

## Intuition
TransNAS-Bench-101 extends NAS benchmarking beyond plain image classification to multiple transfer and dense-prediction tasks.

## Why It Matters
A proxy that only works on one classification setup may fail in broader task families. TransNAS-Bench-101 tests cross-task robustness.

## Tiny Example
A method may rank architectures well on object classification but poorly on semantic segmentation; this benchmark reveals that gap.

## Definition
TransNAS-Bench-101 is a benchmark suite with macro-level and micro-level architecture spaces and pre-evaluated models on Taskonomy-style tasks.

## Key Points
1. Includes multiple tasks and metrics (e.g., Top-1, mIoU).
2. Has macro and micro search spaces.
3. Useful for checking proxy transferability across tasks.

## How This Paper Uses It
- [[RBFleX-NAS]] evaluates object classification and semantic segmentation on both macro and micro spaces.
- Reports Pearson/Kendall plus achieved performance of selected architectures.

## Representative Papers
- [[RBFleX-NAS]]
- TransNAS-Bench-101 benchmark paper.

## Related Concepts
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Activation Function Search]]

