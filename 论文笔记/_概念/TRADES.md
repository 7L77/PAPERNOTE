---
type: concept
aliases: [TRADE-off inspired Adversarial DEfense via Surrogate-loss minimization]
---

# TRADES

## Intuition

TRADES explicitly balances clean accuracy and adversarial robustness during training.

## Why It Matters

Pure adversarial training can overfit robustness and sacrifice clean accuracy; TRADES provides a principled tradeoff objective.

## Tiny Example

Train on clean CE loss plus a KL consistency term between clean and adversarial predictions.

## Definition

TRADES minimizes clean classification loss plus `beta * KL(p_clean || p_adv)` under bounded perturbations.

## Math Form (if needed)

`L = CE(f(x), y) + beta * KL(f(x) || f(x_adv))`.
`x_adv` is generated within an `l_p` threat model.

## Key Points

1. Separates natural-error and robust-error terms.
2. `beta` controls robustness-clean tradeoff.
3. Widely used as strong robust-training baseline.

## How This Paper Uses It

- [[RNAS-CL]]: Uses TRADES as post-search retraining objective to improve adversarial accuracy.

## Representative Papers

- Zhang et al. (2019): TRADES original formulation.

## Related Concepts

- [[Adversarial Robustness]]
- [[PGD Attack]]
