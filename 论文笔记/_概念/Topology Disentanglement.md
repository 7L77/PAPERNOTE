---
type: concept
aliases: [TD in NAS, Topology-Operation Decoupling]
---

# Topology Disentanglement

## Intuition

When architecture search mixes "which edges exist" with "which operation each edge uses," optimization can become inconsistent. Topology disentanglement separates these two decisions.

## Why It Matters

It aligns search-time structure with evaluation-time structure, reducing collapse behaviors caused by topology mismatch.

## Tiny Example

In DARTS-like cells, a node should finally keep 2 input edges. If search always activates all candidate edges, the model trained during search differs from the model evaluated after discretization. TD enforces 2-edge topology already during search.

## Definition

Topology disentanglement introduces separate variables for edge existence and operation choice, then optimizes them with explicit topology constraints.

## Math Form (if needed)

ROME-style notation:
- `B_{i,j}`: whether edge `(i,j)` is selected.
- `A^o_{i,j}`: whether operation `o` on edge `(i,j)` is selected.
- Constraint: each intermediate node has in-degree 2.

## Key Points

1. Decouples edge selection from operation selection.
2. Reduces search-evaluation inconsistency.
3. Often improves robustness of differentiable NAS.

## How This Paper Uses It

- [[ROME]]: uses explicit edge variables (`beta`) and in-degree constraints to prevent topology mismatch collapse.

## Representative Papers

- [[ROME]]: applies TD in single-path differentiable NAS.
- [[DOTS]]: another work that discusses decoupling topology and operations.

## Related Concepts

- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]

