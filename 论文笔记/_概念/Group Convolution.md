---
type: concept
aliases: [Grouped Convolution, GConv]
---

# Group Convolution

## Intuition

Group convolution splits channels into several groups and only connects inputs and outputs within the same group. It saves computation, but it also introduces structural coupling because channels now move in groups rather than as fully independent units.

## Why It Matters

Architectures such as ResNeXt and RegNet use grouped convolutions for efficiency. If we prune them naively channel by channel, we may break the grouped structure or lose the deployability benefits.

## Tiny Example

If a convolution has 64 input channels and 4 groups, each group handles 16 channels. Removing one channel affects the grouping pattern, so practical pruning often removes channels in group-consistent chunks.

## Definition

Group convolution is a convolution operator where the input and output channels are partitioned into groups, and each group performs convolution independently from the others.

## Key Points

1. It reduces connectivity compared with standard dense convolution.
2. It changes what counts as a valid pruning unit.
3. It often creates layer-internal channel coupling.

## How This Paper Uses It

- [[Group Fisher Pruning]]: Treats the input and output channels of grouped convolution as coupled and aggregates their shared-mask gradients accordingly.

## Representative Papers

- [[Group Fisher Pruning]]: Shows how to prune GConv without breaking structural consistency.

## Related Concepts

- [[Channel Pruning]]
- [[Depth-wise Convolution]]
- [[Coupled Channels]]
