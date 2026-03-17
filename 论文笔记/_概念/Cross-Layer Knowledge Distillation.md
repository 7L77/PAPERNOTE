---
type: concept
aliases: [Cross-Layer KD, Layer-wise Teacher-Student Distillation]
---

# Cross-Layer Knowledge Distillation

## Intuition

Instead of forcing the student to copy only the teacher output, we let each student layer learn from a suitable teacher layer.

## Why It Matters

Different layers encode different abstraction levels. Layer-wise matching can transfer richer structure than output-only distillation.

## Tiny Example

A shallow student layer may align with an early teacher edge-pattern layer, while a deep student layer aligns with a semantic teacher layer.

## Definition

Cross-layer KD learns a mapping between student layers and teacher layers, then minimizes a discrepancy (feature/attention/distribution) across mapped pairs.

## Math Form (if needed)

A common form is:
`L = sum_i sum_j g_ij * d(f_s_i, f_t_j)`,
where `g_ij` is a learned match weight, and `d` is a distance (e.g., L2 or KL).

## Key Points

1. Mapping is learned, not manually fixed.
2. Better handles teacher/student depth mismatch.
3. Often implemented with soft-to-hard selection (e.g., Gumbel-Softmax).

## How This Paper Uses It

- [[RNAS-CL]]: Learns per-student-layer tutor assignments and optimizes them jointly with architecture search.

## Representative Papers

- [[RNAS-CL]]: Robust NAS with learnable cross-layer tutor mapping.

## Related Concepts

- [[Knowledge Distillation]]
- [[Attention Map]]
- [[Gumbel-Softmax]]
