---
type: concept
aliases: [Structured Channel Pruning, Channel-level Pruning]
---

# Channel Pruning

## Intuition

Channel pruning means removing entire feature channels instead of removing scattered individual weights. The point is not only to make the model smaller, but to make the network structurally thinner so standard dense kernels can run faster.

## Why It Matters

If we only zero out random weights, the model may look sparse on paper but still run slowly on common hardware. Channel pruning removes whole input/output slices of convolutions, which is much easier to deploy.

## Tiny Example

Suppose a convolution outputs 64 channels, but 16 of them barely change the final prediction. Channel pruning removes those 16 channels completely, so the next layer no longer needs to read or process them.

## Definition

Channel pruning is a structured model compression technique that removes entire channels, filters, or their corresponding tensor slices from a neural network while preserving a valid dense architecture.

## Key Points

1. It is a structured pruning method, unlike unstructured weight sparsity.
2. It often needs fine-tuning after channels are removed.
3. Real acceleration depends on whether the removed channels translate into smaller dense operators.

## How This Paper Uses It

- [[Group Fisher Pruning]]: Extends channel pruning to architectures with cross-layer coupled channels, so pruning remains structurally valid and practically efficient.

## Representative Papers

- [[Group Fisher Pruning]]: Uses Fisher-based global greedy pruning with layer grouping.

## Related Concepts

- [[Coupled Channels]]
- [[Group Convolution]]
- [[Depth-wise Convolution]]
