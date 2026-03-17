---
type: concept
aliases: [Architecture Isomorphism, Cell Isomorphism]
---

# Search Space Isomorphism

## Intuition

Two different architecture encodings can describe effectively the same computation graph. If we count both as different candidates, we overestimate search-space diversity.

## Why It Matters

Isomorphism changes how we interpret search-space size, ranking statistics, and benchmark coverage. It also affects deduplication when building or analyzing NAS benchmarks.

## Tiny Example

In a cell DAG, replacing an edge with `skip-connect` or `zeroize` can collapse nodes/paths so that two encoded cells execute equivalently, even though their edge-op strings differ.

## Definition

Search-space isomorphism refers to equivalence relations over architecture encodings where multiple encoded structures map to the same (or near-equivalent) functional topology under benchmark operation semantics.

## Math Form (if needed)

Let `E` be architecture encodings and `f(e)` map encoding `e` to a canonical graph representation.
Encodings `e1, e2` are isomorphic if `f(e1) = f(e2)` under defined operation-level equivalence rules.

## Key Points

1. Raw encoding count and unique topology count can differ greatly.
2. Isomorphism handling must be explicit; different rules yield different "unique" counts.
3. Ignoring isomorphism may inflate search-space cardinality and bias analysis.

## How This Paper Uses It

- [[NAS-Bench-201]]: Reports `5^6=15625` raw encodings, while appendix analysis shows fewer unique topologies under isomorphism assumptions (e.g., 12751 or 6466 depending on rules).

## Representative Papers

- NAS-Bench-101: Explicitly addresses graph isomorphism in benchmark construction.
- [[NAS-Bench-201]]: Discusses encoding-vs-topology counting differences in appendix.

## Related Concepts

- [[Cell-based Search Space]]
- [[Neural Architecture Search]]
- [[NAS-Bench-201]]
