---
type: concept
aliases: [Micro-batch Gradient Accumulation, Multi-sample Gradient Averaging]
---

# Gradient Accumulation

## Intuition

Instead of updating parameters after one sampled forward/backward pass, we collect gradients from multiple passes and update once. This reduces noise and improves fairness across stochastic samples.

## Why It Matters

In stochastic NAS, one sampled subnetwork can be highly biased. Accumulating over multiple samples per iteration stabilizes optimization.

## Tiny Example

If each iteration samples one path, some operations rarely get trained. Sampling `K=7` paths and accumulating their gradients gives more balanced updates.

## Definition

Gradient accumulation computes gradients over multiple micro-steps (or sampled subnetworks) and combines them (sum or mean) before one optimizer step.

## Math Form (if needed)

For gradient estimates `g_1, ..., g_K`:
\[
\hat{g} = \frac{1}{K}\sum_{k=1}^{K} g_k
\]
If `g_k` are unbiased with variance `\sigma^2`, then `Var(\hat{g}) = \sigma^2 / K`.

## Key Points

1. Reduces gradient variance under stochastic sampling.
2. Improves coverage/fairness for infrequently sampled components.
3. Trades extra compute for better optimization stability.

## How This Paper Uses It

- [[ROME]]: uses two accumulation loops, one for architecture parameters (`alpha`, `beta`) and one for operation weights (`omega`).

## Representative Papers

- [[ROME]]: explicitly ties accumulation to collapse reduction in single-path differentiable NAS.
- [[GDAS]]: baseline single-path method where insufficient sampling motivates ROME's GA extension.

## Related Concepts

- [[Differentiable Architecture Search]]
- [[One-shot NAS]]

