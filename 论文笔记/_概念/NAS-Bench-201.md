---
type: concept
aliases: [NB201, NASBench201]
---

# NAS-Bench-201

## Intuition
NAS-Bench-201 is a compact, fully evaluated NAS search space where many architectures already have recorded training outcomes.

## Why It Matters
It enables fair and reproducible NAS studies without retraining every architecture from scratch.

## Tiny Example
Instead of training 10k candidate architectures on CIFAR-10, researchers query NAS-Bench-201 records to compare search strategies quickly.

## Definition
NAS-Bench-201 is a cell-based search benchmark with a finite architecture set (15,625 raw encodings, 6,466 unique non-isomorphic architectures) and precomputed performance on CIFAR-10/100 and ImageNet16-120.

## Key Points
1. It standardizes comparisons across NAS methods.
2. It is ideal for proxy and predictor analyses.
3. External validity to larger/open spaces must still be tested.

## How This Paper Uses It
- [[ZCP-Eval]]: Uses NAS-Bench-201 as the architecture universe for robustness prediction evaluation.
- [[AZ-NAS]]: Uses NAS-Bench-201 as the primary benchmark for ranking-correlation and selected-architecture evaluation.

## Representative Papers
- [[NAS-Bench-201]]: Original benchmark proposal.
- [[ZCP-Eval]]: Robustness-focused proxy evaluation on this benchmark.

## Related Concepts
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Robust Neural Architecture Search]]
