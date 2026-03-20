---
type: concept
aliases: [Channel Coupling, Coupled Channel Groups]
---

# Coupled Channels

## Intuition

Coupled channels are channels that cannot be pruned independently because the network structure ties them together. If we delete one side but keep the other, the graph becomes inconsistent or the expected speedup does not materialize.

## Why It Matters

Modern CNNs use skip connections, grouped convolutions, and multi-branch heads. In these networks, the useful pruning unit is often not a single layer-local channel, but a set of channels spread across multiple layers.

## Tiny Example

In a residual block, two branches are added element-wise. If channel 5 is removed from one branch but kept in the other, the branch outputs no longer align properly as a deployable compact structure. Those two channel-5 slices are effectively coupled.

## Definition

Coupled channels are channels in one or more layers whose pruning decisions must be synchronized because of graph connectivity, shared downstream usage, or operator constraints such as grouped/depth-wise convolution.

## Key Points

1. Coupling can be cross-layer, not only within one convolution.
2. Residual connections and multi-branch detectors often create coupling.
3. Proper structured pruning should operate on the whole coupled unit.

## How This Paper Uses It

- [[Group Fisher Pruning]]: Introduces layer grouping to automatically discover coupled channels from the computation graph and prune them with shared masks.

## Representative Papers

- [[Group Fisher Pruning]]: Treats coupled channels as the basic pruning unit in complex CNN structures.

## Related Concepts

- [[Channel Pruning]]
- [[Feature Pyramid Network]]
- [[Group Convolution]]
