---
type: concept
aliases: [NB101, NASBench101]
---

# NAS-Bench-101

## Intuition
NAS-Bench-101 is a tabular NAS benchmark that pre-computes the performance of many cell architectures so researchers can compare methods cheaply and reproducibly.

## Why It Matters
It removes expensive full training loops during method comparison and enables fair ranking-evaluation studies.

## Tiny Example
Instead of training every candidate model from scratch, you query NB101 for known accuracy and compute rank correlation against your predictor.

## Definition
NAS-Bench-101 is a benchmark dataset of CNN cell architectures with associated training/validation/test results under fixed protocols.

## Math Form (if needed)
Methods are often evaluated by correlation metrics between predicted score and benchmark ground-truth accuracy.

## Key Points
1. Strong reproducibility for NAS ranking studies.
2. Useful for low-sample predictor evaluation.
3. May not fully reflect transfer to larger or different search spaces.

## How This Paper Uses It
- [[ParZC]]: Evaluates ranking quality and sample efficiency on NB101 (Tab. 1, Tab. 2).

## Representative Papers
- [[ParZC]]: Reports KD/SP improvements and predictor comparisons on NB101.

## Related Concepts
- [[NAS-Bench-201]]
- [[Neural Architecture Search]]
- [[Kendall's Tau]]
