---
type: concept
aliases: [MLP Mixer, Mixer Architecture]
---

# MLP-Mixer

## Intuition
MLP-Mixer alternates mixing over tokens and channels using MLP blocks, without self-attention.

## Why It Matters
It provides a simple and efficient way to model cross-part interactions, which can be repurposed beyond vision patches.

## Tiny Example
Given segmented node statistics, a mixer block can first mix information across segments, then across feature channels.

## Definition
MLP-Mixer is an architecture composed of token-mixing and channel-mixing MLP sublayers, typically with residual and normalization layers.

## Math Form (if needed)
A block often follows:
1) token mixing on transposed input;
2) channel mixing on original layout;
with residual additions after each sublayer.

## Key Points
1. Attention-free yet expressive for global interaction.
2. Works on generic tabular/segment inputs, not only image patches.
3. Performance depends on proper normalization and hidden dimensions.

## How This Paper Uses It
- [[ParZC]]: Uses mixer-style segment interaction for node-wise proxy vectors, plus Bayesian layers.

## Representative Papers
- [[ParZC]]: Adapts mixer structure for NAS ranking from node-wise ZC statistics.

## Related Concepts
- [[Bayesian Neural Network]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
