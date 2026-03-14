---
type: concept
aliases: [Negative Correlation, AZP Negative Correlation]
---

# Negative Correlation in Training-free NAS

## Intuition
A proxy is supposed to rank better architectures higher. Negative correlation means the opposite happens: higher proxy scores correspond to lower true performance.

## Why It Matters
If correlation flips sign, NAS search is actively misled. The search algorithm may consistently move toward worse models.

## Tiny Example
In a deep subspace, architecture A has higher true accuracy than B, but proxy gives A a lower score. If this repeats across many candidates, the search trajectory is reversed.

## Definition
Negative correlation in training-free NAS refers to the phenomenon where zero-cost proxy scores have negative rank correlation (e.g., Spearman rho < 0) with ground-truth architecture performance in a target search space.

## Math Form (if needed)
Typical diagnosis uses Spearman rank correlation:
\[
\rho(\text{proxy scores}, \text{true accuracies}) < 0
\]
which indicates inverted ranking consistency.

## Key Points
1. It can emerge in deeper or more nonlinear architecture subspaces.
2. It is a proxy-design failure, not necessarily a search-algorithm failure.
3. Fixing it often requires score-path redesign (e.g., SAM/NIR).

## How This Paper Uses It
- [[NCD]]: Identifies this as a central failure mode of activation-based proxies and proposes SAM + NIR to correct it.

## Representative Papers
- [[NCD]]: Reports severe sign flip on NAS-Bench-201 subspace 77 and recovers positive correlation.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Stochastic Activation Masking]]
- [[Non-linear Rescaling]]

