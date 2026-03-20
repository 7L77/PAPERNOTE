---
type: concept
aliases: [GIN]
---

# Graph Isomorphism Network

## Intuition
A Graph Isomorphism Network is a graph neural network designed to be very expressive at distinguishing graph structures.

## Why It Matters
If two architectures have meaningfully different graph topology, we want the encoder to notice that. GIN is popular because it is stronger than many simpler graph aggregation schemes in this respect.

## Tiny Example
Two NAS cells may use the same operations but connect them differently. A weaker encoder may blur them together, while GIN is designed to keep those structural differences visible in the embedding.

## Definition
GIN is a message-passing graph neural network whose aggregation and update rule is theoretically connected to the Weisfeiler-Lehman graph isomorphism test, making it highly expressive among common GNN architectures.

## Key Points
1. It is often chosen when graph structure discrimination matters more than geometric smoothness.
2. It usually aggregates neighbor features by sum, then applies an MLP.
3. In NAS encoders, it is useful because architecture graphs differ by both topology and operations.

## How This Paper Uses It
- [[UP-NAS]]: Uses GIN inside the architecture encoder to infer latent means and variances for graph-structured architectures.

## Representative Papers
- Xu et al., "How Powerful are Graph Neural Networks?" (ICLR 2019): Introduces GIN and its expressivity motivation.

## Related Concepts
- [[Variational Graph Autoencoder]]
- [[Architecture Embedding]]
- [[Neural Architecture Search]]

