---
type: concept
aliases: [ADMM, Alternating Direction Method]
---

# Alternating Direction Method of Multipliers

## Intuition
ADMM solves constrained optimization by splitting a hard problem into easier subproblems and coordinating them with dual-variable updates.

## Why It Matters
It is practical when an objective and a constraint are each manageable alone but hard jointly.

## Tiny Example
You want to optimize model loss while enforcing a structured constraint. ADMM alternates: optimize primal variables, then update a dual penalty that pushes constraint satisfaction.

## Definition
ADMM is a first-order optimization framework for problems like
`min f(x)+g(z)` s.t. `Ax+Bz=c`, using augmented Lagrangian and alternating updates on primal and dual variables.

## Math Form (if needed)
Typical steps:
1. `x`-update (with `z,u` fixed)
2. `z`-update (with new `x`, fixed `u`)
3. dual update `u <- u + (Ax+Bz-c)`

## Key Points
1. Decouples coupled objectives/constraints.
2. Often robust in practice for large-scale constrained problems.
3. Hyperparameter (penalty weight) strongly affects convergence behavior.

## How This Paper Uses It
- [[RACL]]: Uses ADMM-style updates to optimize architecture-distribution parameters under confidence-aware Lipschitz constraints.

## Representative Papers
- Boyd et al., "Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers".

## Related Concepts
- [[Confidence Learning]]
- [[Lipschitz Constant]]
- [[Differentiable Architecture Search]]
