---
type: concept
aliases: [Gumbel-Top2, Gumbel Top-k Sampling]
---

# Gumbel-Top-k Reparameterization

## Intuition

Gumbel-Top-k lets us sample the top `k` discrete choices in a stochastic-yet-differentiable way, extending Gumbel-Max (top-1) to multiple selections.

## Why It Matters

Some structure constraints require selecting multiple items at once (for example, choosing exactly two incoming edges). Gumbel-Top-k supports that directly.

## Tiny Example

If a node has 4 candidate predecessor edges and must keep 2, Gumbel-Top2 perturbs each edge log-probability with Gumbel noise and takes the top 2.

## Definition

Given probabilities `p_i` over candidates, draw Gumbel noises `g_i` and rank `log p_i + g_i`; select the top-`k` indices. Softmax-relaxation is used for gradient flow.

## Math Form (if needed)

Core score:
\[
s_i = \log p_i + g_i,\quad g_i \sim \text{Gumbel}(0,1)
\]
Select top-`k` by `s_i`; during training, use a temperature-controlled soft relaxation.

## Key Points

1. Generalizes Gumbel-Max from one choice to multiple choices.
2. Useful under cardinality constraints (exactly `k` selections).
3. Keeps differentiability through continuous relaxation.

## How This Paper Uses It

- [[ROME]]: ROME-v2 uses Gumbel-Top2 to sample exactly two incoming edges per intermediate node.

## Representative Papers

- [[ROME]]: practical use of Gumbel-Top2 for topology sampling in differentiable NAS.
- [[GDAS]]: uses Gumbel-based reparameterization for operation sampling (top-1 style).

## Related Concepts

- [[Differentiable Architecture Search]]
- [[Topology Disentanglement]]

