---
type: concept
aliases: [Square, Black-box Random Search Attack]
---

# Square Attack

## Intuition
Square Attack perturbs square patches of the image using random search, without using gradients.

## Why It Matters
It tests robustness in a black-box setting and can reveal failures that gradient-only attacks might miss.

## Tiny Example
Instead of nudging all pixels by gradient sign, it repeatedly flips small square regions and keeps changes that worsen the model margin.

## Definition
Square Attack is a query-based black-box adversarial attack that optimizes adversarial margin under a norm-constrained perturbation budget.

## Math Form (if needed)
Typical objective under `L_inf`:
\[
\min_{\tilde{x}} \left(f_{y,\theta}(\tilde{x}) - \max_{k\ne y} f_{k,\theta}(\tilde{x})\right),\quad \|\tilde{x}-x\|_\infty \le \epsilon.
\]

## Key Points
1. Does not require model gradients.
2. Query-efficient compared with naive black-box attacks.
3. Complements gradient attacks in robustness evaluation suites.

## How This Paper Uses It
- [[NADR-Dataset]]: Evaluates all non-isomorphic NAS-Bench-201 architectures with Square Attack across multiple epsilon values.

## Representative Papers
- Andriushchenko et al., "Square Attack" (ECCV 2020).
- Croce and Hein, "AutoAttack" (ICML 2020).

## Related Concepts
- [[AutoAttack]]
- [[Adversarial Robustness]]
- [[PGD Attack]]

