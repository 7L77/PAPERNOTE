---
type: concept
aliases: [Architecture Latent, Architecture Representation]
---

# Architecture Embedding

## Intuition
An Architecture Embedding is a continuous vector representation of a neural architecture that preserves useful structural or performance-related information.

## Why It Matters
It lets us compare, predict, cluster, and optimize architectures using standard continuous machine learning tools instead of only discrete combinatorial search.

## Tiny Example
A NAS cell graph can be encoded into a vector `Z`. We can train a predictor on `Z`, or move `Z` with gradients and decode it into a new architecture candidate.

## Definition
An architecture embedding is a latent representation produced by an encoder that maps a discrete neural architecture into a continuous space where nearby points ideally reflect meaningful architectural similarity or search utility.

## Key Points
1. Good embeddings should preserve both topology and operation information.
2. Smoothness matters if we want to optimize in latent space.
3. Embeddings are useful for predictors, clustering, retrieval, and gradient-based NAS.

## How This Paper Uses It
- [[UP-NAS]]: Encodes each architecture into a latent vector, predicts proxy scores from that vector, and performs gradient ascent directly on the vector.

## Representative Papers
- [[NAO]]: Uses continuous architecture representations for predictor-guided search.
- `arch2vec`: Learns unsupervised architecture representations for NAS.

## Related Concepts
- [[Variational Graph Autoencoder]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]

