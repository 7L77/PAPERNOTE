---
type: concept
aliases: [IB, Information-Theoretic Bottleneck]
---

# Information Bottleneck

## Intuition
Information Bottleneck (IB) says a good representation should keep only what is useful for prediction and discard irrelevant details.

## Why It Matters
It provides a principled way to trade off compression and task relevance, which is useful when designing robust or transferable model scores.

## Tiny Example
For classifying cats vs dogs, fur texture and ear shape are useful, while random background noise should be compressed away.

## Definition
Given input `X`, representation `R`, and target `Y`, IB seeks a representation that minimizes `I(R;X)` while preserving `I(R;Y)`.

## Math Form (if needed)
A common objective is:
`L_IB = I(R;X) - beta * I(R;Y)`.
`I` is mutual information and `beta` controls the compression-strength tradeoff.

## Key Points
1. IB balances compression and predictive utility.
2. Larger `beta` usually forces stronger compression.
3. Many practical methods approximate IB with entropy/divergence surrogates.

## How This Paper Uses It
- [[IBFS]]: Derives an entropy-driven zero-cost architecture score from an IB objective for few-shot NAS.

## Representative Papers
- Tishby et al. (2000): Introduced the IB principle.
- [[IBFS]]: Applies IB to training-free architecture ranking.

## Related Concepts
- [[Entropy]]
- [[KL Divergence]]
- [[Zero-Cost Proxy]]
