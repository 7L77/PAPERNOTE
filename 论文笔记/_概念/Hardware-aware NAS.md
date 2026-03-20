---
type: concept
aliases: ["Efficient NAS", "Device-aware NAS"]
---

# Hardware-aware NAS

## Intuition

Hardware-aware NAS does not search only for accuracy. It searches for architectures that are accurate enough and also fit a target device in latency, energy, memory, or throughput.

## Why It Matters

In deployment, the best model is rarely the one with the highest test accuracy alone. A model that is too slow or too power-hungry is unusable on the target hardware.

## Tiny Example

A CNN with slightly lower accuracy but 2x lower latency on Jetson TX2 may be preferable to a more accurate but much slower model in an edge deployment setting.

## Definition

Hardware-aware NAS is NAS under explicit hardware objectives or constraints, where architecture search must optimize both task performance and device-side efficiency metrics.

## Key Points

1. Accuracy and hardware efficiency must be optimized jointly rather than sequentially.
2. Pareto analysis is often more meaningful than single-score ranking.
3. Good hardware-aware NAS usually depends on both an accuracy proxy and a hardware performance model.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: studies zero-shot proxies under energy and latency constraints and shows that ranking gets harder in relaxed high-accuracy regions.

## Representative Papers

- [[Zero-shot NAS Survey]]: survey and hardware-aware proxy comparison.
- [[HW-NAS-Bench]]: benchmark widely used for hardware-aware NAS evaluation.

## Related Concepts

- [[Hardware Performance Model]]
- [[Pareto Frontier]]

