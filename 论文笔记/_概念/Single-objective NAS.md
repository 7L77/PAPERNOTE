---
type: concept
aliases: [SONAS, Single Objective Neural Architecture Search]
---

# Single-objective NAS

## Intuition
Single-objective NAS optimizes one scalar target, such as validation accuracy, and returns one best architecture.

## Why It Matters
It is simple and easy to compare, but it can hide trade-offs between conflicting goals like robustness, cost, and accuracy.

## Tiny Example
If the objective is `Val-Acc-12`, the search may pick a model with high early accuracy but not necessarily the best adversarial robustness.

## Definition
SONAS solves:
\[
\min_{x \in \mathcal{A}} f(x),
\]
where \(f\) is a single objective over architecture \(x\) in search space \(\mathcal{A}\).

## Key Points
1. Returns one optimum for one objective.
2. Easier optimization setup than multi-objective NAS.
3. Can miss useful trade-off architectures.

## How This Paper Uses It
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Uses GA-based SONAS variants (`Val-Acc-12` and `SynFlow`) as baselines.

## Representative Papers
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Reports that training-based SONAS objective often beats SynFlow-based SONAS after adversarial training evaluation.

## Related Concepts
- [[Multi-objective NAS]]
- [[Genetic Algorithm]]

