---
type: concept
aliases: [Operator-Importance Pruning NAS, Rank-based Pruning NAS]
---

# Pruning-by-Importance NAS

## Intuition
Instead of sampling and training many whole architectures, this idea asks a finer question: which operator is least important on each edge right now? Then it removes low-importance operators iteratively.

## Why It Matters
It turns a combinatorial architecture search problem into a sequence of local elimination decisions, often reducing search cost substantially.

## Tiny Example
If one edge has 5 operators, and deleting operator A improves trainability while barely hurting expressivity, A gets a low importance score and is pruned first.

## Definition
Pruning-by-importance NAS is a search strategy that starts from an over-parameterized supernet and repeatedly prunes candidate operators according to an importance score estimated from proxy signals.

## Math Form (if needed)
A common form is rank-sum importance:

$$
s(o_j) = s_1(o_j) + s_2(o_j)
$$

where `s_1`, `s_2` are ranking indices from different proxies (for example trainability and expressivity). Lower `s(o_j)` means higher chance to prune.

## Key Points
1. Reduces search space progressively instead of evaluating full candidates from scratch.
2. Quality depends on the reliability of importance proxies.
3. Easy to combine multiple proxies through rank-based aggregation.

## How This Paper Uses It
- [[TE-NAS]]: computes NTK- and linear-region-based ranking signals per operator removal and prunes edge-wise.

## Representative Papers
- [[TE-NAS]]: canonical training-free rank-pruning NAS example.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
