---
type: concept
aliases: ["Optimization Ease", "Convergence Behavior"]
---

# Trainability

## Intuition

Trainability asks whether the network can be optimized smoothly and efficiently. A trainable network is one where gradients propagate sensibly and optimization does not immediately stall or collapse.

## Why It Matters

Even a very expressive architecture is not useful if optimization is unstable. Many zero-shot proxies focus on trainability because it leaves measurable traces at initialization.

## Tiny Example

If one architecture quickly suffers from vanishing or exploding gradients while another keeps gradients well-scaled across layers, the second is usually easier to train.

## Definition

Trainability is the degree to which a network architecture supports stable gradient propagation, efficient optimization, and convergence to good solutions under practical training procedures.

## Key Points

1. Gradient-based proxies often target trainability more than anything else.
2. Better trainability does not automatically imply better generalization.
3. Architecture topology, width, and skip connections strongly affect trainability.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: treats trainability as one of the three core proxy-design axes and shows that many successful proxies mainly capture this property.

## Representative Papers

- [[Zero-shot NAS Survey]]: uses trainability as a central lens for proxy analysis.
- [[How does topology influence gradient propagation and model performance of deep networks with DenseNet-type skip connections?]]: representative topology-trainability work referenced by the survey.

## Related Concepts

- [[Expressive Capacity]]
- [[Generalization Capacity]]

