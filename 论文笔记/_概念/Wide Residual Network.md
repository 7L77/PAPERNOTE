---
type: concept
aliases: [WRN, Wide ResNet]
---

# Wide Residual Network

## Intuition
Wide Residual Network (WRN) increases residual block width instead of only stacking more layers, trading extreme depth for stronger per-layer capacity and easier optimization.

## Why It Matters
WRN is a common robust-training backbone. Many adversarial robustness studies and benchmarks analyze how depth-width choices in WRN affect robustness.

## Tiny Example
`WRN-34-10` means a 34-layer residual network with a width multiplier of 10, often much wider than standard ResNet variants at similar depth.

## Definition
A ResNet-family architecture that scales channel width by a factor `k` and usually uses fewer but wider residual blocks, often written as `WRN-depth-width`.

## Math Form (if needed)
If a stage base channel is `n_i`, WRN stage channel can be represented as `k * n_i`, where `k` is width factor.

## Key Points
1. Width scaling can improve representation power and training behavior.
2. WRN provides a clean axis to study depth-width tradeoffs.
3. In robust learning, WRN variants are standard experimental backbones.

## How This Paper Uses It
- [[NARes]]: Uses WRN macro design as the entire search space and enumerates stage-wise depth/width combinations.

## Representative Papers
- Zagoruyko and Komodakis (2017): Original WRN paper.
- [[NARes]]: Large-scale robust benchmark over WRN macro space.

## Related Concepts
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
