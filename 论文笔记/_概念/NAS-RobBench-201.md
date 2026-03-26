---
type: concept
aliases: [NAS RobBench 201, Robust NAS-Bench-201]
---

# NAS-RobBench-201

## Intuition
NAS-RobBench-201 is a robust NAS benchmark that records architecture performance after adversarial training, not just standard training.

## Why It Matters
It lets us compare robust NAS algorithms quickly and reproducibly without retraining every architecture from scratch.

## Tiny Example
You can query one architecture’s clean accuracy, FGSM accuracy, PGD accuracy, and AutoAttack accuracy directly from the benchmark table.

## Definition
NAS-RobBench-201 extends NAS-Bench-201-style tabular evaluation with adversarial-training-aware robustness metrics across multiple attacks.

## Key Points
1. It emphasizes robustness after adversarial training.
2. It supports large-scale algorithm comparisons with low compute overhead.
3. It can change conclusions compared with non-AT robustness datasets.

## How This Paper Uses It
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Uses NAS-RobBench-201 as the main evaluation source for clean/robust metrics.

## Representative Papers
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Studies GA/NSGA-II objective choices with this benchmark.

## Related Concepts
- [[NAS-Bench-201]]
- [[Adversarial Training]]

