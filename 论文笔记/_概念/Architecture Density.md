---
type: concept
aliases: [Density of Architecture Connectivity, Graph Density in NAS]
---

# Architecture Density

## Intuition
Architecture Density measures how many edges are active in a network graph. A denser architecture has more information paths, which may improve robustness by offering redundant feature routes.

## Why It Matters
It turns an abstract topology preference ("dense connections are better") into a measurable scalar used for robust architecture analysis.

## Tiny Example
If a cell has 14 possible edges and one architecture activates 11 edges while another activates 6, the first has higher density and is often observed as more robust in RobNet's study.

## Definition
Given architecture edges `E` and active edges `E_connected`, density is
\[
D=\frac{|E_{connected}|}{|E|}
\]
In RobNet's binary edge-operation parameterization:
\[
D=\frac{\sum_{i,j,k}\alpha^{(i,j)}_k}{|E|}
\]
where `alpha` indicates whether an operation on an edge is active.

## Key Points
1. It is a topology-level metric independent of final parameter values.
2. Higher density correlates with higher adversarial accuracy in RobNet's sampled architectures.
3. It is descriptive and diagnostic, not a standalone robustness guarantee.

## How This Paper Uses It
- [[RobNet]]: Uses architecture density to explain why densely connected patterns tend to be more robust.

## Representative Papers
- [[RobNet]]: Empirically validates density-robustness correlation on sampled architectures.

## Related Concepts
- [[Neural Architecture Search]]
- [[Cell-based Search Space]]
- [[Adversarial Robustness]]

