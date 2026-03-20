---
type: concept
aliases: [Agglomerative Clustering, HAC]
---

# Hierarchical Agglomerative Clustering

## Intuition
HAC starts with each sample as its own cluster and repeatedly merges the closest clusters, building a tree (dendrogram) from leaves to root.

## Why It Matters
It produces a hierarchy directly, which is useful when downstream algorithms need tree-structured decisions instead of flat partitions.

## Tiny Example
Given architecture output vectors, HAC can group functionally similar architectures first, then merge broader groups, yielding a search tree.

## Definition
Given pairwise distances, HAC iteratively merges clusters according to a linkage rule (e.g., Ward linkage) until one cluster remains.

## Key Points
1. Outputs a full hierarchy, not just one partition.
2. Strongly depends on distance metric and linkage rule.
3. Typical implementation cost is quadratic in sample count.

## How This Paper Uses It
- [[MCTS-Learned Hierarchy]] computes pairwise distances between architecture outputs and uses agglomerative clustering to build the MCTS tree (Sec.4, Algorithm 1).

## Representative Papers
- Murtagh and Legendre (2014): Ward hierarchical clustering discussion.

## Related Concepts
- [[Monte-Carlo Tree Search]]
- [[KL Divergence]]
- [[Neural Architecture Search]]
