---
type: concept
aliases: [Weight Sharing in NAS, One-shot Weight Sharing]
---

# Parameter Sharing in NAS

## Intuition

Instead of training every candidate architecture from scratch, parameter-sharing NAS trains a supernet once and lets many sub-architectures reuse its weights. This makes search much cheaper, but shared weights are usually not equally good for all candidates.

## Why It Matters

It is one of the key reasons NAS became computationally feasible. Many differentiable and one-shot NAS methods depend on it for practical runtime.

## Tiny Example

If two candidate cells both include a `3x3 conv` edge, supernet training lets them reuse the same edge weights. You avoid training each candidate independently, but ranking quality can degrade if shared weights favor some structures.

## Definition

Parameter sharing in NAS is a strategy where a common set of network parameters is jointly optimized across many architecture candidates, and candidate evaluation is approximated using those shared parameters instead of individually trained weights.

## Math Form (if needed)

Let architecture choices be `a in A`, shared weights be `W`, and validation score be `R(a, W)`.
Supernet training optimizes `W` over sampled architectures:

`min_W E_{a~p(a)} [ L_train(a, W) ]`

Then search uses proxy ranking from `R(a, W)` to pick architecture(s), rather than fully retraining each `a`.

## Key Points

1. Major speedup source for one-shot and differentiable NAS.
2. Ranking bias is common because `W` is not optimal for every candidate.
3. BN-statistics handling and sampling strategy strongly affect ranking fidelity.

## How This Paper Uses It

- [[NAS-Bench-201]]: Uses the benchmark to compare parameter-sharing methods against non-parameter-sharing methods and shows sensitivity to BN handling (Sec. 5, Table 5, Table 7, Fig. 7-8).

## Representative Papers

- One-shot NAS family (e.g., ENAS): Early large-scale demonstration of parameter sharing.
- Differentiable NAS family (e.g., DARTS): Continuous relaxation with shared weights.
- [[NAS-Bench-201]]: Provides controlled evidence of parameter-sharing failure modes and evaluation caveats.

## Related Concepts

- [[One-shot NAS]]
- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]
