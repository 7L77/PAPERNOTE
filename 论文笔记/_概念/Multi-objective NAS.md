---
type: concept
aliases: [MONAS, Multi-Objective Neural Architecture Search]
---

# Multi-objective NAS

## Intuition
Multi-objective NAS optimizes multiple goals at once, such as accuracy, robustness, and FLOPs, and returns a set of trade-off architectures.

## Why It Matters
Real deployment rarely has one goal. MONAS makes trade-offs explicit instead of collapsing everything into one score.

## Tiny Example
One architecture may be best in robustness while another is best in latency. MONAS keeps both on a Pareto set.

## Definition
MONAS seeks non-dominated architectures under vector objectives:
\[
\min_{x \in \mathcal{A}} [f_1(x), f_2(x), ..., f_k(x)].
\]

## Key Points
1. Outputs a Pareto set rather than one model.
2. Better at exposing accuracy-robustness-efficiency trade-offs.
3. Needs a decision rule to select a final deployment model.

## How This Paper Uses It
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Uses NSGA-II MONAS variants and selects representatives via aggregate ranking.

## Representative Papers
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Shows `NSGA-II (SynFlow)` outperforms `NSGA-II (Val-Acc-12)` on all reported metrics.

## Related Concepts
- [[NSGA-II]]
- [[Pareto Front]]

