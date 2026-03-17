---
type: concept
aliases: [Activation Attention Map, Spatial Attention Map]
---

# Attention Map

## Intuition

An attention map tells us where a model is focusing in the input space.

## Why It Matters

It turns hidden activations into an interpretable spatial signal that can be aligned across models.

## Tiny Example

If a classifier predicts "car," attention map highlights wheels/body regions rather than sky/background.

## Definition

Given feature tensor `A in R^{C x H x W}`, a common map is `F(A) in R^{H x W}` by channel aggregation.

## Math Form (if needed)

In [[RNAS-CL]], attention map is:
`[F(A)]_{h,w} = sum_c A_{c,h,w}^2`.

## Key Points

1. It is a derived representation, not a standalone module.
2. Different aggregation rules exist (sum, abs-sum, norm-based).
3. Useful for interpretation and distillation constraints.

## How This Paper Uses It

- [[RNAS-CL]]: Uses normalized attention-map distance in cross-layer teacher-student alignment.

## Representative Papers

- [[RNAS-CL]]: Integrates attention-map alignment into robust NAS.

## Related Concepts

- [[Knowledge Distillation]]
- [[Cross-Layer Knowledge Distillation]]
