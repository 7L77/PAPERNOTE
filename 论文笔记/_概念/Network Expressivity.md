---
type: concept
aliases: [Model Expressivity, Function Expressivity]
---

# Network Expressivity

## Intuition
Network expressivity describes how rich or flexible the functions represented by a network can be.

## Why It Matters
In NAS, highly expressive architectures are often better at fitting complex data patterns, though too much capacity can hurt efficiency or generalization.

## Tiny Example
A shallow linear model can only draw a single decision boundary, while a deeper ReLU network can form many piecewise-linear regions.

## Definition
For piecewise-linear networks (e.g., ReLU networks), expressivity is often linked to how many distinct linear regions the network can partition the input space into.

## Key Points
1. Expressivity is about representational capacity, not guaranteed final accuracy.
2. Depth and width both affect expressivity.
3. Activation-pattern-based proxies estimate expressivity without full training.

## How This Paper Uses It
- [[SWAP-NAS]]: Uses unique sample-wise activation patterns as an expressivity proxy.

## Representative Papers
- [[SWAP-NAS]]: Connects expressivity estimation with training-free NAS ranking.

## Related Concepts
- [[Sample-Wise Activation Pattern]]
- [[Zero-Cost Proxy]]

