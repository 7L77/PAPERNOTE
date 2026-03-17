---
type: concept
aliases: [Isomorphic Graphs in NAS, Architecture Canonicalization]
---

# Isomorphic Architectures

## Intuition
Two architecture encodings can look different as strings but compute the same function graph.

## Why It Matters
If not deduplicated, benchmark statistics can double-count effectively identical networks and bias search/evaluation.

## Tiny Example
A skip edge can make another edge operation irrelevant, so two different edge-label assignments become equivalent.

## Definition
In NAS graph spaces, two architectures are isomorphic if there exists a node/edge correspondence preserving computation semantics, yielding equivalent functional graphs.

## Math Form (if needed)
Let `G1` and `G2` be computation graphs. They are isomorphic if there exists a bijection `phi` such that adjacency and operation labels are preserved under `phi` up to semantic equivalence.

## Key Points
1. Canonical IDs are needed for fair tabular benchmarks.
2. Isomorphism reduction shrinks search spaces substantially.
3. Mapping functions (`id -> uid`) are essential for downstream querying.

## How This Paper Uses It
- [[NADR-Dataset]]: Starts from 15,625 NAS-Bench-201 encodings and keeps 6,466 non-isomorphic architectures for evaluation.

## Representative Papers
- Dong and Yang, "NAS-Bench-201" (2020).
- Jung et al., "Neural Architecture Design and Robustness: A Dataset" (2023).

## Related Concepts
- [[NAS-Bench-201]]
- [[Neural Architecture Search]]
- [[NADR-Dataset]]

