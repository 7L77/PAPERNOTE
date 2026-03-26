---
type: concept
aliases: [Piecewise Linear Regions, Activation Regions]
---

# Linear Regions

## Intuition

For ReLU networks, the input space is partitioned into many pieces. Inside each piece, the network behaves like a linear function. Each piece is called a linear region.

## Why It Matters

The number of linear regions is often used as a rough proxy for expressivity: more regions usually mean the network can model more complex decision boundaries.

## Tiny Example

A 1D ReLU network with one hidden ReLU splits the line at a hinge point. That creates two linear regions (left/right of hinge).

## Definition

For a fixed parameter setting \(\theta\), each activation pattern \(P\) defines a subset of inputs where all neuron pre-activation signs match \(P\). Non-empty subsets are linear regions.

## Key Points

1. Linear regions depend on both architecture and current parameters.
2. More regions generally imply higher representational flexibility, but not guaranteed robustness by itself.
3. In robust NAS, region count is useful when combined with trainability indicators.

## How This Paper Uses It

- [[RTP-NAS]]: uses linear-region count with adversarial NTK condition number to rank operators during pruning.

## Representative Papers

- [[RTP-NAS]]: uses linear regions as one of two key pruning metrics.
- [[Training-free NAS]]: broader family where cheap structure-aware indicators are used during search.

## Related Concepts

- [[Neural Tangent Kernel]]
- [[Condition Number]]
- [[Expressive Capacity]]
- [[Training-free NAS]]
