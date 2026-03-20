---
type: concept
aliases: [VGAE, Graph VAE]
---

# Variational Graph Autoencoder

## Intuition
A Variational Graph Autoencoder learns a compact latent representation of a graph and then reconstructs graph structure from that latent code.

## Why It Matters
It lets us move from discrete graph objects to continuous vectors, which is extremely useful when we want to optimize graphs with gradient-based methods.

## Tiny Example
If a neural architecture is represented as a DAG, a VGAE can map it to a latent vector `Z`. We can then update `Z` with gradients and decode it back to a new architecture.

## Definition
A VGAE is a variational autoencoder specialized for graphs. It uses a graph encoder to infer latent variables for nodes or whole graphs, and a decoder to reconstruct edges and node attributes while regularizing the latent space with a KL term.

## Key Points
1. It bridges discrete graph structures and continuous optimization.
2. The KL term encourages a smoother latent space than plain autoencoders.
3. Decoder quality matters: poor reconstruction breaks downstream search.

## How This Paper Uses It
- [[UP-NAS]]: Reuses a VGAE-style architecture autoencoder from `arch2vec` so architectures can be optimized in a continuous latent space and decoded back afterward.

## Representative Papers
- Kipf and Welling, "Variational Graph Auto-Encoders" (2016): Canonical VGAE formulation.

## Related Concepts
- [[Architecture Embedding]]
- [[Graph Isomorphism Network]]
- [[Neural Architecture Search]]

