---
type: concept
aliases: [Weight Update Consistency, Parameter Similarity under Perturbation]
---

# Parameter Consistency

## Intuition
If clean and perturbed tasks drive parameters in similar directions, optimization is less conflicting.

## Why It Matters
Consistent update geometry usually indicates the architecture can jointly support clean and robust objectives.

## Tiny Example
After one SGD step on clean and perturbed losses, compare `theta_1` and `theta_1^r`; high cosine similarity suggests consistency.

## Definition
Parameter consistency measures similarity between parameter states (or updates) obtained from clean and perturbed objectives.

## Key Points
1. It approximates optimization compatibility between tasks.
2. One-step estimates are cheap but informative.
3. It complements feature-level signals.

## How This Paper Uses It
- [[CRoZe]] defines `P_m(theta_1, theta_1^r)` as a layer-wise parameter similarity term (Eq. 8).

## Representative Papers
- [[CRoZe]]

## Related Concepts
- [[Feature Consistency]]
- [[Gradient Alignment]]
- [[Robust Neural Architecture Search]]
