---
type: concept
aliases: [Pareto Frontier, Non-dominated Set]
---

# Pareto Front

## Intuition
Pareto front is the boundary of best tradeoff solutions. Moving from one point to another usually improves one objective but worsens another.

## Why It Matters
For deployment, there is rarely one universally best model. Pareto front gives a menu of budget-aware choices.

## Tiny Example
If you want fewer parameters, you may lose some accuracy. A Pareto point is one where no other candidate is both smaller and more accurate.

## Definition
A solution is Pareto-optimal if no other feasible solution improves one objective without degrading at least one other objective.

## Key Points
1. It captures tradeoffs instead of single-score ranking.
2. It depends on the chosen objectives.
3. It is the natural output of multi-objective NAS.

## How This Paper Uses It
- [[LLaMA-NAS]]: Reports adapter candidates on the accuracy-parameter Pareto frontier.

## Representative Papers
- [[LLaMA-NAS]]: Uses Pareto front to pick deployable adapter subnetworks.

## Related Concepts
- [[NSGA-II]]
- [[Neural Architecture Search]]
