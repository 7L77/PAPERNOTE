---
type: concept
aliases: [Gradient Alignment Correlation, Trace Correlation Proxy]
---

# Gradient Trace Correlation

## Intuition
If a pruned model still points in similar gradient directions as the pretrained base model on the same data, it is more likely to recover performance quickly.

## Why It Matters
For pretrained-model pruning, we care less about "can it train from scratch" and more about "does it preserve functional behavior." Gradient-trace correlation is a direct signal for that.

## Tiny Example
Compute gradients of base and pruned model on a small calibration set, standardize them, and compare by Pearson correlation per layer. High correlation means stronger functional inheritance.

## Definition
Gradient trace correlation measures directional consistency between aggregated gradient traces of two models (typically base vs. pruned) over the same data distribution.

## Math Form (if needed)
\[
g = \mathbb{E}_{b \in B}[\nabla_\theta \mathcal{L}(M(b;\theta))]
\]
\[
\rho^{(l)}=\mathrm{Pearson}\left(g_{sub}^{(l)}, g_{base}^{(l)}\right)
\]
It is often aggregated across layers, optionally with sparsity/importance weights.

## Key Points
1. It is direction-focused rather than magnitude-focused.
2. Pearson normalization makes it robust to pruning-induced scale shifts.
3. It can be used as a zero-shot ranking proxy for architecture search.

## How This Paper Uses It
- [[TraceNAS]] defines a sparsity-weighted aggregation of per-layer gradient-trace correlations as the core proxy `Phi`.

## Representative Papers
- [[TraceNAS]]: Introduces this proxy for zero-shot LLM structured pruning search.

## Related Concepts
- [[Gradient Alignment]]
- [[Pearson Correlation Coefficient]]
- [[Training-free NAS]]
