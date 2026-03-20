---
type: concept
aliases: [Shannon Entropy, Information Entropy]
---

# Entropy

## Intuition
Entropy measures uncertainty: higher entropy means the distribution is more spread out and less predictable.

## Why It Matters
Entropy is a core information-theoretic quantity used in regularization, uncertainty analysis, and proxy construction.

## Tiny Example
A fair coin has higher entropy than a biased coin that lands heads 99% of the time.

## Definition
For discrete distribution `p`, Shannon entropy is `H(p) = -sum_i p_i log p_i`.

## Math Form (if needed)
If all `K` classes are equally likely, entropy is maximal at `log K`.

## Key Points
1. Captures uncertainty, not correctness by itself.
2. Depends on the full distribution shape.
3. Often appears in IB, calibration, and zero-cost proxy design.

## How This Paper Uses It
- [[IBFS]]: Uses entropy over Jacobian-spectrum-derived distributions as architecture expressivity score.

## Representative Papers
- Shannon (1948): Foundational entropy definition.
- [[IBFS]]: Entropy-based training-free NAS ranking.

## Related Concepts
- [[Information Bottleneck]]
- [[KL Divergence]]
- [[Zero-Cost Proxy]]
