---
type: concept
aliases: [Cross Attention, Multi-head Cross-Attention]
---

# Cross-Attention

## Intuition
Cross-attention lets one representation query another representation, so the model can condition decisions in one modality/space on information from another.

## Why It Matters
In NAS surrogate modeling, we often need metric features and architecture features to interact. Cross-attention gives a direct way to learn this interaction.

## Tiny Example
Use architecture embedding as query and metric embeddings as key/value. The model learns which metrics are most relevant for this architecture.

## Definition
Cross-attention computes attention weights between a query set \(Q\) and a separate key-value set \((K,V)\), producing context-aware outputs for \(Q\).

## Math Form (if needed)
\[
\mathrm{Attn}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
\]

- \(Q\): query vectors.
- \(K,V\): key/value vectors from another source.
- \(d\): key dimension scale factor.

## Key Points
1. Enables conditional fusion between different feature sources.
2. Multi-head form captures different interaction patterns.
3. Usually stronger than naive concatenation when interactions are complex.

## How This Paper Uses It
- [[PO-NAS]]: Uses multi-head cross-attention to connect architecture embeddings with metric embeddings and produce architecture-specific metric weights.

## Representative Papers
- [[Attention Is All You Need]]: Introduces attention framework that underlies cross-attention use.
- [[PO-NAS]]: Applies cross-attention to architecture-specific metric fusion in NAS.

## Related Concepts
- [[Graph Attention Network]]
- [[Surrogate Predictor]]
- [[Zero-Cost Proxy]]
