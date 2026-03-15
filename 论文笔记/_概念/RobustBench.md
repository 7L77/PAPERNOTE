---
type: concept
aliases: [Robust NAS Benchmark in DARTS Space]
---

# RobustBench

## Intuition
RobustBench is a robustness-oriented architecture benchmark used to evaluate how well NAS proxies and search strategies predict adversarial robustness.

## Why It Matters
Adversarial training for every candidate architecture is very costly. A fixed benchmark of pre-evaluated architectures enables fair and efficient method comparison.

## Tiny Example
TRNAS evaluates whether R-Score ranks architectures consistently with RobustBench robust-accuracy statistics before spending full search budget.

## Definition
In the TRNAS context, RobustBench (introduced in ZCPRob) contains 223 adversarially trained architectures sampled from the DARTS search space, with associated adversarial accuracies.

## Key Points
1. It is mainly for robust NAS analysis, not generic vision benchmark reporting.
2. It provides pre-computed robust metrics under common attacks.
3. It helps compare training-free robustness proxies without re-training all candidates.

## How This Paper Uses It
- [[TRNAS]] uses RobustBench to evaluate R-Score quality and compare with robust NAS baselines.

## Representative Papers
- [[ZCPRob]]: introduces RobustBench in robust zero-cost proxy context.
- [[TRNAS]]: uses RobustBench for robust proxy validation and search analysis.

## Related Concepts
- [[Adversarial Robustness]]
- [[DARTS]]
- [[Zero-Cost Proxy]]
- [[NAS-Rob-Bench-201]]

