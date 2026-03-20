---
type: concept
aliases: [tieredImageNet, tiered-ImageNet Benchmark]
---

# tiered-ImageNet

## Intuition
tiered-ImageNet is an ImageNet-based few-shot benchmark with higher semantic diversity and larger scale than mini-ImageNet.

## Why It Matters
Its hierarchical split is designed to test stronger cross-class generalization in few-shot settings.

## Tiny Example
Even if support and query classes are unseen during training, they come from broader ImageNet hierarchies, making transfer harder.

## Definition
tiered-ImageNet contains many more images/classes than mini-ImageNet and uses superclass-aware splits for FSL evaluation.

## Math Form (if needed)
Like mini-ImageNet, results are reported over many sampled N-way K-shot episodes.

## Key Points
1. Harder and larger-scale FSL benchmark.
2. Better stress-test for generalization than mini-ImageNet alone.
3. Frequently paired with mini-ImageNet in papers.

## How This Paper Uses It
- [[IBFS]]: Reports 5-way 1-shot/5-shot accuracy and search-cost comparisons on tiered-ImageNet.

## Representative Papers
- Ren et al. (2018): Introduced tiered-ImageNet benchmark.
- [[IBFS]]: Uses it for cross-benchmark FSL validation.

## Related Concepts
- [[Few-shot Learning]]
- [[mini-ImageNet]]
