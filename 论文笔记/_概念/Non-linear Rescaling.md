---
type: concept
aliases: [NIR, Nonlinear Rescaling]
---

# Non-linear Rescaling

## Intuition
When activation-based proxies sum too many nonlinear responses, their scores can lose ranking meaning. NIR re-stabilizes this response scale so proxy scores remain informative.

## Why It Matters
Without rescaling, deeper architectures may get artificially suppressed scores, causing wrong ranking and negative correlation with true accuracy.

## Tiny Example
Two architectures differ in quality, but both produce saturated proxy values after many ReLU+BN layers. NIR changes the normalization path so scores recover separation.

## Definition
In [[NCD]], NIR is motivated by theoretical analysis of BN/LN aggregation. The method uses a normalization/rescaling strategy (LN-oriented during AZP evaluation) to reduce nonlinear amplification and improve correlation robustness.

## Math Form (if needed)
The paper derives BN/LN mean terms as weighted sums of ReLU activations (Eq. (5)-(10), Theorem 4.1/4.2), then argues LN-style handling at initialization can mitigate nonlinear accumulation.

## Key Points
1. NIR targets score-scale pathology rather than model expressivity itself.
2. It complements SAM: SAM reduces sampled activation load, NIR stabilizes normalization effect.
3. It is especially useful in deep or high-FLOPs subspaces.

## How This Paper Uses It
- [[NCD]]: Applies NIR with SAM to convert negative correlation back to positive correlation on deep NAS-Bench-201 subspaces.

## Representative Papers
- [[NCD]]: Introduces the NIR treatment in Sec. 4.2 and validates it with ablations.

## Related Concepts
- [[Stochastic Activation Masking]]
- [[Negative Correlation in Training-free NAS]]
- [[Zero-Cost Proxy]]

