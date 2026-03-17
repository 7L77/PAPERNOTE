---
type: concept
aliases: [Concrete Distribution, Differentiable Categorical Sampling]
---

# Gumbel-Softmax

## Intuition

It gives a differentiable way to choose from discrete options during gradient-based training.

## Why It Matters

NAS often needs discrete architecture decisions; Gumbel-Softmax enables end-to-end optimization before hard selection.

## Tiny Example

Instead of choosing one channel option directly, we optimize soft weights over all options and gradually sharpen them.

## Definition

For logits `v_i`, sampled Gumbel noises `g_i`, and temperature `tau`,
`y_i = exp((v_i+g_i)/tau) / sum_j exp((v_j+g_j)/tau)`.
As `tau -> 0`, it approaches one-hot argmax behavior.

## Math Form (if needed)

Same expression above; practical training uses annealed `tau`.

## Key Points

1. Bridges discrete choice and gradient descent.
2. Temperature controls softness vs discreteness.
3. Can use hard sampling in later stages.

## How This Paper Uses It

- [[RNAS-CL]]: Uses Gumbel-Softmax for both tutor-layer assignment and channel/filter search.

## Representative Papers

- Jang et al. (2017): Original Gumbel-Softmax reparameterization.
- [[RNAS-CL]]: Applies it in robust NAS with cross-layer distillation.

## Related Concepts

- [[Neural Architecture Search]]
- [[Cross-Layer Knowledge Distillation]]
