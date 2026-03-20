---
type: concept
aliases: ["Pareto Front", "Pareto-optimal Set"]
---

# Pareto Frontier

## Intuition

When we care about two objectives at once, such as accuracy and latency, there is usually no single best model. The Pareto frontier is the set of models where you cannot improve one objective without worsening the other.

## Why It Matters

Hardware-aware NAS is almost always multi-objective. Pareto analysis tells us whether a search method is finding good tradeoffs rather than just optimizing one metric in isolation.

## Tiny Example

If model A is more accurate and no slower than model B, then B is dominated and should not lie on the Pareto frontier. A frontier model survives only if it offers a real tradeoff.

## Definition

The Pareto frontier is the subset of candidate solutions that are non-dominated under a set of competing objectives, meaning no other solution is strictly better in all objectives at once.

## Key Points

1. It is the right language for accuracy-efficiency tradeoffs.
2. Under relaxed hardware constraints, finding the true frontier becomes harder because high-accuracy ranking matters more.
3. A proxy can have decent global correlation yet still recover a poor Pareto frontier.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: compares proxy-selected networks against the ground-truth Pareto frontier under energy and latency constraints.

## Representative Papers

- [[Zero-shot NAS Survey]]: analyzes Pareto quality in hardware-aware zero-shot NAS.
- [[HW-NAS-Bench]]: benchmark often used to study Pareto tradeoffs with hardware costs.

## Related Concepts

- [[Hardware-aware NAS]]
- [[Hardware Performance Model]]

