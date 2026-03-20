---
type: concept
aliases: [Listwise Loss, Ranking List Optimization]
---

# Listwise Ranking Loss

## Intuition

Listwise ranking loss treats a ranked list as a whole object, and optimizes consistency between predicted list order and ground-truth list order.

## Why It Matters

In NAS, selecting top candidates depends on full-list behavior, not just isolated pair decisions. Listwise objectives can capture this global structure.

## Tiny Example

For four architectures, pairwise constraints might all look mostly correct, but top-1 can still be wrong. Listwise loss penalizes this full-order mismatch directly.

## Definition

A representative listwise loss is [[ListMLE]], which assigns likelihood to the full ground-truth permutation and maximizes it.

## Math Form (if needed)

- Input: predicted scores over a list.
- Target: ground-truth ranking permutation.
- Objective: maximize probability of generating the true ranking list.

## Key Points

1. Optimizes global ordering consistency.
2. Usually more aligned with ranking tasks than pointwise regression.
3. Can be used as warm-up before top-focused weighted losses.

## How This Paper Uses It

- [[PWLNAS]]: uses ListMLE as listwise representative and combines it with WARP in NAS-Bench-101 piecewise loss.

## Representative Papers

- [[PWLNAS]]: large-scale benchmark of listwise vs pairwise vs weighted losses for NAS predictors.

## Related Concepts

- [[ListMLE]]
- [[Pairwise Ranking Loss]]
