---
type: concept
aliases: [SAM, Activation Masking]
---

# Stochastic Activation Masking

## Intuition
Instead of always using every activation value in convolution scoring, SAM randomly masks part of them each time. This reduces over-accumulated non-linearity in proxy evaluation.

## Why It Matters
For activation-based zero-cost proxies, too much non-linearity can invert ranking correlation. SAM is a cheap way to stabilize the score signal.

## Tiny Example
If a proxy always sums all ReLU outputs in deep blocks, scores can collapse. With SAM (`alpha=0.9`), only a sampled subset contributes per pass, reducing saturation and preserving ranking contrast.

## Definition
SAM introduces a Bernoulli mask tensor \(M\) into activation-based convolution scoring:
\[
y = \sum(W \odot M \odot X),\quad M(i,j,k)\sim Bernoulli(1-\alpha)
\]
where `alpha` controls masking ratio.

## Math Form (if needed)
- \(W\): convolution kernel weights
- \(X\): input activation tensor
- \(M\): random mask tensor
- \(\odot\): Hadamard product
- \(\alpha\in[0,1]\): masking hyperparameter

## Key Points
1. SAM is stochastic and lightweight, not a heavy architectural change.
2. It aims to control non-linearity accumulation during proxy scoring.
3. It is typically combined with normalization/rescaling strategies (e.g., NIR).

## How This Paper Uses It
- [[NCD]]: Uses SAM as the first component to mitigate negative correlation in activation-based training-free NAS.

## Representative Papers
- [[NCD]]: Formalizes SAM with Eq. (4) and validates gains in Table 7.

## Related Concepts
- [[Non-linear Rescaling]]
- [[Negative Correlation in Training-free NAS]]
- [[Zero-Cost Proxy]]

