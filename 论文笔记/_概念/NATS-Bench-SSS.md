---
type: concept
aliases: [NATS-SSS]
---

# NATS-Bench-SSS

## Intuition
NATS-Bench-SSS is a NAS benchmark where architectures differ mainly by network size settings, enabling fast and reproducible proxy evaluation.

## Why It Matters
It provides a standardized large candidate pool for comparing ranking/sampling behavior across NAS methods.

## Tiny Example
A training-free proxy can score thousands of SSS candidates quickly, then query benchmark ground-truth accuracy for correlation analysis.

## Definition
NATS-Bench contains search spaces for NAS research. The SSS split (size search space) focuses on architecture scaling variants with precomputed performance on multiple datasets.

## Key Points
1. Useful for robust statistics over many candidates.
2. Supports CIFAR-10 / CIFAR-100 / ImageNet16-120 style evaluations.
3. Frequently used to report Pearson/Kendall correlation of training-free proxies.

## How This Paper Uses It
- [[RBFleX-NAS]] uses NATS-Bench-SSS as one of its main evaluation spaces.
- Reports both correlation metrics and architecture search outcomes under multiple sample sizes.

## Representative Papers
- [[RBFleX-NAS]]
- NATS-Bench benchmark paper.

## Related Concepts
- [[NAS-Bench-201]]
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]

