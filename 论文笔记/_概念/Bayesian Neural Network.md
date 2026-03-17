---
type: concept
aliases: [Bayesian NN, BNN]
---

# Bayesian Neural Network

## Intuition
A Bayesian Neural Network treats weights as probability distributions, not fixed numbers.

## Why It Matters
This allows uncertainty estimation, which is useful when input statistics are noisy or limited.

## Tiny Example
Instead of one weight value `w=0.8`, BNN learns a distribution around 0.8; predictions can report both score and confidence.

## Definition
BNN models posterior distributions over neural network weights and marginalizes over these distributions during prediction.

## Math Form (if needed)
A common reparameterization is:
\[
W = \mu + \sigma \odot \epsilon,\quad \epsilon \sim \mathcal{N}(0,I)
\]

## Key Points
1. Explicitly models epistemic uncertainty.
2. Can improve robustness in low-data settings.
3. Usually more expensive than deterministic networks.

## How This Paper Uses It
- [[ParZC]]: Inserts Bayesian layers around mixer blocks to estimate uncertainty in node-wise ZC statistics.

## Representative Papers
- [[ParZC]]: Applies Bayesian layers in a NAS ranking predictor.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
- [[Kendall's Tau]]
