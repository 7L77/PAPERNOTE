---
type: concept
aliases: [TPE, Tree Structured Parzen Estimator]
---

# Tree-structured Parzen Estimator

## Intuition
Tree-structured Parzen Estimator is a black-box hyperparameter search method that tries to learn which regions of parameter space look promising, then samples more often from those regions.

## Why It Matters
When an objective is expensive or non-differentiable, TPE gives a practical way to search good hyperparameters without exhaustive enumeration.

## Tiny Example
Suppose we want proxy weights for 13 zero-cost metrics. Instead of checking every combination, TPE keeps track of which weight settings lead to higher rank correlation and proposes the next settings accordingly.

## Definition
TPE is a sequential model-based optimization method that models `p(x | y)` and `p(y)` rather than directly modeling `p(y | x)`, then chooses new configurations that are likely to improve the objective.

## Key Points
1. It works well for non-convex, mixed, and non-differentiable hyperparameter spaces.
2. It is commonly used through tools like Optuna.
3. Its output quality depends on the evaluation budget and the stability of the target metric.

## How This Paper Uses It
- [[UP-NAS]]: Uses TPE to search the proxy-combination weights `lambda` that maximize [[Kendall's Tau]] on NAS-Bench-201-CIFAR-10.

## Representative Papers
- Bergstra et al., "Algorithms for Hyper-Parameter Optimization" (NeurIPS 2011): Introduces the TPE framework.

## Related Concepts
- [[Kendall's Tau]]
- [[Unified Proxy]]
- [[Zero-Cost Proxy]]

