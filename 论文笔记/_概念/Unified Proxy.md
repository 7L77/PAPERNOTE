---
type: concept
aliases: [UP, Proxy Fusion Score]
---

# Unified Proxy

## Intuition
A Unified Proxy is a single score formed by combining multiple zero-cost proxies so that search is driven by one consolidated objective instead of many separate, sometimes conflicting signals.

## Why It Matters
Different zero-cost proxies capture different aspects of architecture quality. A unified score can reduce single-proxy bias and make search behavior more stable.

## Tiny Example
If `jacov` is good at expressivity, `synflow` reflects trainability, and `params` should be penalized, a unified proxy can assign positive and negative weights to combine them into one ranking score.

## Definition
A unified proxy is an aggregate scalar scoring function, often weighted, built from several proxy metrics to better align with true architecture performance than any single metric alone.

## Key Points
1. It can be a simple weighted sum or a more adaptive fusion rule.
2. Its value depends heavily on how weights are learned and transferred.
3. It is attractive because it lets search use one scalar objective while still leveraging multiple proxy signals.

## How This Paper Uses It
- [[UP-NAS]]: Defines `UP(A)=sum_i lambda_i f^i_zc(A)` and uses the resulting scalar as the search objective in latent-space gradient ascent.

## Representative Papers
- [[UP-NAS]]: Early explicit unified-proxy formulation for training-free NAS.
- [[PO-NAS]]: Later work that also studies multi-proxy fusion, but with architecture-specific weighting.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Tree-structured Parzen Estimator]]

