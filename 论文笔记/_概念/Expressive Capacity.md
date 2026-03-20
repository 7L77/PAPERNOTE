---
type: concept
aliases: ["Model Expressivity", "Representation Capacity"]
---

# Expressive Capacity

## Intuition

Expressive capacity asks how rich a family of functions a network can represent. A more expressive network can carve up the input space in more flexible ways and fit more complex patterns.

## Why It Matters

If a network is not expressive enough, no optimization trick will rescue it on a hard task. Many zero-shot proxies try to estimate this property because it is one ingredient of final accuracy.

## Tiny Example

A deeper or wider ReLU network can partition the input space into more linear regions than a very small network, so it can model more complicated decision boundaries.

## Definition

Expressive capacity is the ability of a neural network architecture to represent a broad and complex class of functions or input-output mappings.

## Key Points

1. High expressivity helps only when paired with trainability and generalization.
2. Metrics based on linear regions or Jacobian structure often aim to capture expressivity.
3. A model can be highly expressive but still hard to optimize or poor at generalization.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: treats expressive capacity as one of the three required dimensions for a good proxy.

## Representative Papers

- [[Zero-shot NAS Survey]]: links expressivity to linear-region and Jacobian-style proxies.
- [[Zen-NAS]]: uses an initialization statistic that the survey interprets as expressivity-related.

## Related Concepts

- [[Trainability]]
- [[Generalization Capacity]]

