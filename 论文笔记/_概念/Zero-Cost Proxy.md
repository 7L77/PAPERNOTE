---
type: concept
aliases: [ZCP, Zero Cost Proxy]
---

# Zero-Cost Proxy

## Intuition
A Zero-Cost Proxy is a cheap signal computed on an untrained or barely trained network to estimate how good the architecture may become after full training.

## Why It Matters
Full architecture evaluation is expensive. ZCPs make large-scale architecture screening practical.

## Tiny Example
Given two candidate cells in NAS, if `jacov` score for A is much higher than B, A is prioritized for deeper evaluation before spending full training budget.

## Definition
A ZCP is a scalar or low-dimensional statistic derived from architecture structure and/or one/few forward-backward passes at initialization time, used as a surrogate feature for architecture performance prediction.

## Key Points
1. ZCPs are usually low-compute and fast.
2. Their reliability can differ by task (clean accuracy vs robustness).
3. Combining multiple ZCPs often outperforms single-proxy usage.

## How This Paper Uses It
- [[ZCP-Eval]]: Uses 15 ZCPs as regression features to predict clean and robust accuracy.
- [[AZ-NAS]]: Builds a multi-proxy training-free NAS score by combining expressivity, progressivity, trainability, and complexity.

## Representative Papers
- [[ZCP-Eval]]: Systematic robustness-oriented evaluation of ZCP transferability.
- [[NAS-Bench-Suite-Zero]]: Benchmarking and comparing many ZCPs across tasks.

## Related Concepts
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
- [[Robust Neural Architecture Search]]
