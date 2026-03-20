---
type: concept
aliases: [DARTS-style NAS, Gradient-based NAS]
---

# Differentiable Architecture Search

## Intuition

Instead of trying architectures one by one from scratch, differentiable NAS builds a supernet and turns architecture choices into continuous variables so we can optimize them with gradients.

## Why It Matters

It drastically reduces search cost compared with reinforcement learning or evolutionary NAS, making architecture search practical on limited compute.

## Tiny Example

Suppose an edge can choose either `3x3 conv` or `skip`. DARTS-style methods assign soft weights to both and learn these weights during training, then keep the stronger one when discretizing.

## Definition

Differentiable Architecture Search parameterizes discrete architectural decisions with continuous relaxation (often softmax/Gumbel-softmax) and optimizes architecture parameters jointly or bi-level with network weights.

## Math Form (if needed)

Typical form on one edge:
\[
\bar{o}(x) = \sum_{o \in \mathcal{O}} \text{softmax}(\alpha)_o \cdot o(x)
\]
where `alpha` are architecture parameters and `o` are candidate operations.

## Key Points

1. It converts combinational search into gradient optimization.
2. It often uses bi-level optimization (weights on train split, architecture on val split).
3. Relaxation-discretization mismatch can cause instability or collapse.
4. In the canonical DARTS cell, each edge in a DAG mixes candidate operations with softmax weights over architecture parameters.
5. The usual objective is `min_alpha L_val(w*(alpha), alpha)` with `w*(alpha) = argmin_w L_train(w, alpha)`, so architecture and supernet weights stay tightly coupled during search.

## How This Paper Uses It

- [[ROME]]: starts from single-path differentiable NAS and fixes collapse by topology disentanglement plus gradient accumulation.
- [[LLMENAS]]: uses DARTS in the preliminaries to restate the standard continuous-relaxation setup, then contrasts it with evolutionary search because DARTS can prefer parameter-free operations such as skip connections and get trapped in local optima.
- [[LLMENAS]]: in Section III.B, the point is not to improve DARTS directly, but to establish the baseline formulation that later motivates replacing gradient-driven search dynamics with CMA-ES plus LLM-designed fitness guidance.

## Representative Papers

- [[DARTS]]: canonical formulation of differentiable architecture search.
- [[GDAS]]: single-path differentiable NAS with Gumbel sampling.
- [[LLMENAS]]: uses DARTS as the reference gradient-based baseline that motivates a hierarchical evolutionary alternative.

## Related Concepts

- [[Neural Architecture Search]]
- [[One-shot NAS]]
