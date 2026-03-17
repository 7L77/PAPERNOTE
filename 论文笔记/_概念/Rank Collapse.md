---
type: concept
aliases: [Rank Degeneration, Low-rank Collapse]
---

# Rank Collapse

## Intuition
Rank collapse means representations become less diverse as layers stack deeper, eventually behaving like almost rank-1 outputs. In plain terms, many tokens/features start carrying nearly the same information.

## Why It Matters
If representations collapse to low rank, model expressivity drops. For NAS, collapse severity can become a useful signal of architecture quality.

## Tiny Example
Suppose a 4-token sequence is projected across many layers and every token vector becomes nearly parallel. Even if values differ slightly, the model effectively sees one direction only, so discrimination power degrades.

## Definition
Given feature matrix `X`, rank collapse refers to the phenomenon where `rank(X)` (or effective rank) decreases with depth, often approaching 1 in extreme cases.

## Math Form (if needed)
One common view is distance to the nearest rank-1 matrix:
\[
\min_{u,v} \|X - uv^\top\|
\]
Smaller distance indicates stronger collapse.

## Key Points
1. It is a depth-related representation degeneration effect.
2. Regularization layers can mitigate but may not fully eliminate it.
3. It can be turned into a training-free proxy signal.

## How This Paper Uses It
- [[TF-MAS]]: assumes stacked SSD blocks in Mamba2 also exhibit rank-collapse tendency, then builds a proxy around this behavior.

## Representative Papers
- [[TF-MAS]]: transfers rank-collapse-inspired proxy design to Mamba2 NAS.

## Related Concepts
- [[Effective Rank]]
- [[State Space Duality (SSD)]]
- [[Training-free NAS]]

