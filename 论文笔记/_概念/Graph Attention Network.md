---
type: concept
aliases: [GAT, Graph Attention Networks]
---

# Graph Attention Network

## Intuition
A Graph Attention Network (GAT) learns node representations by weighting neighbors differently, instead of averaging all neighbors equally.

## Why It Matters
Architecture graphs in NAS have structured connectivity. GAT can emphasize more informative edges/nodes when building architecture embeddings.

## Tiny Example
For a node in a cell graph, GAT can assign high attention to predecessor nodes carrying key operations and low attention to less informative ones.

## Definition
GAT is a graph neural network where attention coefficients are computed on graph edges and used to aggregate neighbor features into updated node states.

## Key Points
1. Neighbor importance is learned, not fixed.
2. Multi-head attention improves stability and expressiveness.
3. Works well when edge-local structure matters for downstream tasks.

## How This Paper Uses It
- [[PO-NAS]]: Uses a two-layer GAT encoder to produce architecture embeddings during pretraining before surrogate BO/evolution stages.

## Representative Papers
- [[Graph Attention Networks]]: Original GAT paper.
- [[PO-NAS]]: Uses GAT for architecture encoding in NAS metric fusion.

## Related Concepts
- [[Cross-Attention]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
