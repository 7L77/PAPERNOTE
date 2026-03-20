---
type: concept
aliases: [Piecewise Loss, Staged Loss Schedule]
---

# Piecewise Loss Function

## Intuition

A piecewise loss function changes optimization objective by stage, instead of using one fixed loss from start to end.

## Why It Matters

In iterative NAS search, data distribution and sample size evolve over time. A fixed loss may be good early but suboptimal later.

## Tiny Example

Early training uses ranking loss to stabilize ordering with few samples; later training switches to weighted loss to emphasize top candidates.

## Definition

A generic form:
\[
\mathcal{L}(t)=
\begin{cases}
\mathcal{L}_{warm}, & t \le t_{warm}\\
\mathcal{L}_{focus}, & t > t_{warm}
\end{cases}
\]
where \(t\) can be iteration count or queried-sample count.

## Math Form (if needed)

- \(\mathcal{L}_{warm}\): objective for low-data stage.
- \(\mathcal{L}_{focus}\): objective for later focused stage.
- \(t_{warm}\): switching threshold.

## Key Points

1. It is a schedule over objectives, not only over learning rate.
2. Useful when optimization targets differ across search stages.
3. Requires careful threshold and loss-pair design.

## How This Paper Uses It

- [[PWLNAS]]: core method uses piecewise loss to combine early ranking/regression benefits with later weighted-loss benefits.

## Representative Papers

- [[PWLNAS]]: demonstrates practical gains of staged loss switching across multiple NAS benchmarks.

## Related Concepts

- [[Pairwise Ranking Loss]]
- [[MAPE Loss]]
