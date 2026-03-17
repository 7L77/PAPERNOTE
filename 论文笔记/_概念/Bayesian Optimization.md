---
type: concept
aliases: [BO, BayesOpt]
---

# Bayesian Optimization

## Intuition
Bayesian Optimization is a strategy for optimizing expensive black-box objectives by learning a cheap probabilistic surrogate and querying only a small number of promising points.

## Why It Matters
When each evaluation is expensive (e.g., training a NAS candidate), BO can dramatically reduce trial count while still finding strong solutions.

## Tiny Example
Suppose each architecture training run costs hours. BO fits a surrogate over tried architectures, then picks the next one balancing high predicted performance and uncertainty.

## Definition
Bayesian Optimization iteratively builds a probabilistic model (often a Gaussian Process or learned surrogate), then maximizes an acquisition policy to decide where to evaluate the true objective next.

## Key Points
1. Best for low-budget optimization of expensive functions.
2. Exploration-exploitation balance is controlled by acquisition behavior.
3. Quality depends heavily on surrogate calibration.

## How This Paper Uses It
- [[PO-NAS]]: Uses a BO-like iterative loop to update a surrogate from limited true performance labels and pick new architectures for real training.

## Representative Papers
- [[BOHB]]: Combines BO with bandit-style resource allocation.
- [[BANANAS]]: Neural predictor-based BO for architecture search.

## Related Concepts
- [[Surrogate Predictor]]
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]
