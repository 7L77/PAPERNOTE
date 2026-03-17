---
type: concept
aliases: [Parameter Entanglement, Weight Reuse Entanglement]
---

# Weight Entanglement

## Intuition
Weight entanglement reuses subsets of pretrained model parameters to initialize many sampled candidate architectures, so we can evaluate many structures quickly without training each from scratch.

## Why It Matters
Constructing NAS benchmarks for large models is expensive. Weight entanglement provides a practical shortcut for large-scale proxy correlation studies.

## Tiny Example
Given a pretrained 130M model, if a sampled candidate is narrower or shallower, we activate the corresponding slices of pretrained weights, then do short fine-tuning instead of full training.

## Definition
Weight entanglement is a parameter-sharing initialization strategy: candidate architectures inherit compatible parameter subsets from a reference pretrained model to reduce evaluation cost.

## Math Form (if needed)
No single canonical formula. Conceptually, it defines a mapping
\[
\theta_{candidate} \leftarrow \mathcal{S}(\theta_{reference}, A_{candidate})
\]
where `\mathcal{S}` slices/aligns weights by candidate architecture `A`.

## Key Points
1. It reduces benchmark construction cost dramatically.
2. It may introduce noise in measured candidate performance.
3. Noise can bias rank-correlation estimates conservatively.

## How This Paper Uses It
- [[TF-MAS]]: uses weight entanglement to build Mamba2 NASBenches (500 architectures each) and then fine-tunes briefly for practical correlation estimation.

## Representative Papers
- [[TF-MAS]]: uses entanglement to make Mamba2 benchmark construction feasible.

## Related Concepts
- [[Super-network]]
- [[Evolutionary Neural Architecture Search]]
- [[Training-free NAS]]

