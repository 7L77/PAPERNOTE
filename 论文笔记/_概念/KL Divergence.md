---
type: concept
aliases: [Kullback-Leibler Divergence, Relative Entropy]
---

# KL Divergence

## Intuition

KL divergence measures how different one probability distribution is from another.

## Why It Matters

It is a core tool for distillation and robustness objectives that compare model output distributions.

## Tiny Example

If teacher and student output the same class probabilities, KL is near zero; larger mismatch gives higher KL.

## Definition

For distributions `P` and `Q`, `KL(P||Q) = sum_i P(i) log(P(i)/Q(i))`.

## Math Form (if needed)

`KL(P||Q) >= 0`, and equals zero only when `P=Q` almost everywhere.

## Key Points

1. Asymmetric divergence (`KL(P||Q) != KL(Q||P)`).
2. Sensitive to places where `Q` assigns tiny probability.
3. Widely used in KD and TRADES-like losses.

## How This Paper Uses It

- [[RNAS-CL]]: Uses KL term between student and teacher output distributions in search/train objectives.

## Representative Papers

- [[RNAS-CL]]: Applies KL in robust NAS distillation objective.

## Related Concepts

- [[Knowledge Distillation]]
- [[TRADES]]
