---
type: concept
aliases: ["Latency Predictor", "Hardware Cost Predictor"]
---

# Hardware Performance Model

## Intuition

A hardware performance model predicts how a network will behave on a device before we actually deploy and benchmark it there. It is the hardware-side analogue of an accuracy proxy.

## Why It Matters

Real device measurements are expensive and often unavailable at scale. Without a good latency or energy predictor, hardware-aware NAS becomes slow, noisy, or impossible to run broadly.

## Tiny Example

Instead of measuring latency for every candidate network on a mobile GPU, we train or fit a predictor that estimates latency from the architecture structure and hardware descriptors.

## Definition

A hardware performance model is a predictive model or lookup system that estimates device-side metrics such as latency, energy, memory, or throughput for candidate neural architectures.

## Key Points

1. It complements the accuracy proxy in hardware-aware NAS.
2. Prediction granularity can be layer-level or kernel-level.
3. Transferability across devices is often as important as raw prediction error.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: compares BRP-NAS, HELP, and NN-Meter and treats hardware modeling as a first-class part of the NAS pipeline.

## Representative Papers

- [[Zero-shot NAS Survey]]: summarizes major hardware prediction models.
- [[NN-Meter]]: representative kernel-level latency predictor.

## Related Concepts

- [[Hardware-aware NAS]]
- [[NAS Benchmark]]

