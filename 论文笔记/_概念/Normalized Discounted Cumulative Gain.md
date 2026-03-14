---
type: concept
aliases: [nDCG, NDCG]
---

# Normalized Discounted Cumulative Gain

## Intuition

nDCG measures ranking quality with extra emphasis on top positions. Putting highly relevant items early is rewarded more than placing them late.

## Why It Matters

In NAS we care most about whether a proxy can surface the best architectures quickly. Metrics that treat all pair orders equally may miss this top-heavy objective.

## Tiny Example

If two rankings have similar global correlation but one swaps the top 2 models with lower-quality ones, nDCG drops sharply while rank correlation may not drop as much.

## Definition

nDCG is the discounted cumulative gain (DCG) normalized by the ideal DCG so the score lies in `[0,1]`.

## Math Form (if needed)

VKDNW uses:

`nDCG_P = (1/Z) * sum_{j=1..P} (2^{acc_{k_j}} - 1) / log2(1+j)` (Sec. III, Eq. (14)).

`P` is the top cutoff and `Z` is the ideal normalization constant.

## Key Points

1. nDCG is position-sensitive and top-heavy by design.
2. It is often more practical for search/retrieval-style tasks than pure correlation.
3. Choice of `P` should match the practical shortlist size.

## How This Paper Uses It

- [[VKDNW]]: Proposes nDCG as a companion metric for TF-NAS proxy evaluation.

## Representative Papers

- [[VKDNW]]: Demonstrates nDCG can reveal top-ranking failures hidden by KT/SPR.

## Related Concepts

- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Fisher Information Matrix]]
