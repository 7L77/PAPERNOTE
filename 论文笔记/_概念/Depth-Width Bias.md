---
type: concept
aliases: [Depth Bias, Width-Depth Bias, Deep-Narrow Bias]
---

# Depth-Width Bias

## Intuition

Depth-Width Bias means a ranking rule or search process systematically prefers making a network deeper instead of wider, even when that preference does not actually produce the best final model.

## Why It Matters

In NAS, the search algorithm only sees the score it is given. If that score over-rewards depth, the search can get trapped around overly deep and narrow models and miss better balanced architectures.

## Tiny Example

Suppose model A has 80 layers with small channels and model B has 50 layers with healthier width. If a zero-cost proxy adds up layer contributions, A may get a larger score simply because it has more layers, even though B trains to higher accuracy after full training.

## Definition

Depth-Width Bias is the tendency of an architecture metric, proxy, or search heuristic to assign disproportionately favorable scores to deeper networks relative to wider ones under a fixed compute or search setting.

## Math Form (if needed)

There is no single universal formula. In practice, the bias often appears when:

1. the score is accumulated over layers, so depth is counted repeatedly;
2. width contributes only weakly or indirectly;
3. the search loop trusts that score as the main ranking signal.

## Key Points

1. It is a property of the proxy-plus-search-space combination, not only of the network family.
2. The bias is especially visible in repeated-block micro-architecture search.
3. A proxy can have decent benchmark correlation and still suffer from depth-width bias during actual search.

## How This Paper Uses It

- [[ZiCo-BC]]: identifies that original ZiCo over-favors deeper and thinner models in repeated-block search spaces, then adds a structural penalty to correct it.

## Representative Papers

- [[ZiCo-BC]]: makes the bias explicit and proposes a practical correction term for zero-shot NAS.

## Related Concepts

- [[Width-Depth Ratio]]
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
