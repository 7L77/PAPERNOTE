---
type: concept
aliases: [TPC, Path Count Proxy]
---

# Total Path Count

## Intuition

Total Path Count (TPC) estimates how many distinct input-to-output computational paths an architecture can form.

## Why It Matters

It provides a very fast architecture expressivity proxy for zero-shot NAS without training each candidate.

## Tiny Example

If every unit in layer A can connect to many units in layer B, and this repeats over layers, total end-to-end paths grow multiplicatively.

## Definition

TPC score is computed by estimating per-layer path counts and aggregating across layers; practical implementations often sum log path counts to avoid numeric explosion.

## Math Form (if needed)

In GEN-TPC-NAS, the global TPC score is:

\[
S_t = \sum_p \log(O_p)
\]

where \(O_p\) is path count of layer \(p\).

## Key Points

1. TPC is a structural proxy derived from architecture parameters only.
2. It emphasizes expressivity, not directly generalization.
3. It is suitable for fast filtering in large search spaces.

## How This Paper Uses It

- [[GEN-TPC-NAS]]: Uses TPC score in the first search stage and as a minimum threshold in the second stage.

## Representative Papers

- [[TPC-NAS]]: Introduces TPC-based zero-shot architecture ranking.

## Related Concepts

- [[Network Expressivity]]
- [[Zero-Cost Proxy]]

