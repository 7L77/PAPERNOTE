---
type: concept
aliases: [Nondominated Sorting Genetic Algorithm II, NSGA2]
---

# NSGA-II

## Intuition
NSGA-II is a multi-objective evolutionary search algorithm. Instead of forcing all goals into one score, it keeps a population of candidates and preserves those that are not dominated on any objective.

## Why It Matters
When we care about both accuracy and model size, a single scalar score often hides tradeoffs. NSGA-II returns a set of choices across the tradeoff boundary.

## Tiny Example
Model A is more accurate but larger, Model B is smaller but slightly less accurate. Both can survive in NSGA-II because neither strictly dominates the other.

## Definition
NSGA-II performs non-dominated sorting and crowding-distance based selection to evolve a population toward an approximate Pareto front.

## Key Points
1. It is population-based and multi-objective by design.
2. It uses dominance ranking plus diversity preservation.
3. It outputs a set of Pareto candidates, not one model.

## How This Paper Uses It
- [[LLaMA-NAS]]: Uses NSGA-II to search adapter architectures under performance and parameter objectives.

## Representative Papers
- [[LLaMA-NAS]]: Applies NSGA-II to mixed-rank adapter architecture search.

## Related Concepts
- [[Pareto Front]]
- [[Neural Architecture Search]]
