---
type: concept
aliases: [Precision at T, Top-T Precision]
---

# Precision@T

## Intuition

Precision@T asks a simple question: among the top T items selected by a scoring method, how many are truly top T under the ground truth target?

## Why It Matters

In NAS and ranking problems, we often care more about whether the shortlist is good than whether the entire global ranking is perfect.

## Tiny Example

Suppose T=5. Your proxy ranks architectures and picks top 5. If 3 of those are also in the real top 5 by full training accuracy, then Precision@5 is 3/5=0.6.

## Definition

Given ranking \(R_M\) from proxy metric \(M\) and ranking \(R_f\) from true objective \(f\):

\[
\rho_T(M,f)=\frac{|\{A \mid R_M(A)\le T \land R_f(A)\le T\}|}{T}
\]

It measures overlap ratio between proxy top-T and true top-T.

## Math Form (if needed)

- \(A\): candidate architecture.
- \(R_M(A)\): rank of \(A\) under proxy metric.
- \(R_f(A)\): rank of \(A\) under true objective.
- \(T\): top-k cutoff.

## Key Points

1. It focuses on shortlist quality, not full-list correlation.
2. It is directly aligned with budgeted search where only top candidates are queried.
3. Two methods can have similar global rank correlation but very different Precision@T.

## How This Paper Uses It

- [[RoBoT]]: uses Precision@T to quantify estimation gap and justify greedy exploitation over top-ranked architectures.

## Representative Papers

- [[RoBoT]]: formalizes Precision@T in its robustify-then-exploit NAS pipeline.

## Related Concepts

- [[Training-free NAS]]
- [[Kendall's Tau]]
