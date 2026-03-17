---
type: concept
aliases: [SSD, Structured State Space Duality]
---

# State Space Duality (SSD)

## Intuition
SSD is a formulation that rewrites selective state-space computation in a form closely related to attention-style tensor operations, making some analysis tools transferable between the two worlds.

## Why It Matters
For Mamba2, SSD is the core computational block. Understanding SSD enables us to reason about expressivity, rank behavior, and architecture-level proxy design.

## Tiny Example
In attention, we often reason with `Q/K/V` interactions. In SSD-based Mamba2, analogous tensors (`C/B/X` in TF-MAS notation) interact through structured operations, so some attention insights can still apply.

## Definition
SSD refers to the dual representation of selective state-space model computations used in Mamba2, where sequence transformation can be expressed via matrix/tensor compositions that parallel linear-attention-like patterns.

## Math Form (if needed)
In TF-MAS paper notation, SSD output is described in a compact matrix form such as
\[
Y = (L \circ (CB^\top))X
\]
where `L` is a structured term and `\circ` denotes elementwise interaction in the paper's formulation.

## Key Points
1. SSD is the computational heart of Mamba2 blocks.
2. It enables comparing Mamba2 behavior with attention behavior.
3. It provides the bridge that TF-MAS uses for rank-collapse-inspired proxy design.

## How This Paper Uses It
- [[TF-MAS]]: treats stacked SSD as rank-collapse-prone and derives a Mamba2-specific training-free proxy from SSD internal mappings.

## Representative Papers
- [[TF-MAS]]: uses SSD internals for architecture scoring.

## Related Concepts
- [[Rank Collapse]]
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]

