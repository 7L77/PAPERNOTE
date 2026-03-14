---
type: concept
aliases: [Cell NAS Space, Cell Topology Space]
---

# Cell-based Search Space

## Intuition
Instead of searching a full deep network end-to-end, NAS searches a small repeated cell, then stacks it to form the final model.

## Why It Matters
This design drastically reduces search complexity and allows transfer of searched cell structures across datasets.

## Tiny Example
A cell is represented as a DAG with operations on edges (e.g., 3x3 conv, 1x1 conv, skip). NAS optimizes this DAG, then repeats it many times.

## Definition
A cell-based search space defines architecture candidates by the micro-structure of one or a few cell graphs, while macro-depth is usually fixed or separately configured.

## Key Points
1. Search focuses on micro topology and operation choices.
2. Final network is produced by stacking searched cells.
3. Common in DARTS-style NAS and benchmark suites.

## How This Paper Uses It
- [[SWAP-NAS]]: Uses DARTS-style cell encoding and evolutionary operations on adjacency-matrix-like representations.

## Representative Papers
- [[SWAP-NAS]]: Integrates regularized SWAP score with cell-based evolutionary search.

## Related Concepts
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]

