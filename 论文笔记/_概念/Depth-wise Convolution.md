---
type: concept
aliases: [Depthwise Convolution, DWConv]
---

# Depth-wise Convolution

## Intuition

Depth-wise convolution applies one spatial filter per input channel instead of mixing channels densely. It is computationally cheap, but because each channel is handled separately, pruning decisions interact strongly with the layer structure.

## Why It Matters

Mobile-friendly architectures such as MobileNet rely on depth-wise convolution. If a pruning method only works for standard dense convolutions, it misses a major family of practical efficient networks.

## Tiny Example

In a depth-wise layer with 32 channels, each channel has its own spatial filter. Removing one channel removes both its input pathway and its dedicated spatial filter, so the pruning action is structurally significant.

## Definition

Depth-wise convolution is a special case of grouped convolution where the number of groups equals the number of input channels, so each input channel is convolved independently.

## Key Points

1. It is an extreme grouped-convolution case.
2. It is central to lightweight CNN design.
3. Pruning it requires respecting the one-channel-per-group structure.

## How This Paper Uses It

- [[Group Fisher Pruning]]: Extends the grouping-and-shared-mask logic to depth-wise convolution so MobileNetV2-style networks can be pruned effectively.

## Representative Papers

- [[Group Fisher Pruning]]: Demonstrates pruning on MobileNetV2 and treats DWConv as a structurally coupled case.

## Related Concepts

- [[Group Convolution]]
- [[Channel Pruning]]
- [[Coupled Channels]]
