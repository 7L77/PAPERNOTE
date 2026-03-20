---
type: concept
aliases: [miniImageNet, mini-ImageNet Benchmark]
---

# mini-ImageNet

## Intuition
mini-ImageNet is a compact ImageNet-derived benchmark widely used for few-shot classification.

## Why It Matters
It became the standard testbed for comparing few-shot methods under consistent N-way K-shot protocols.

## Tiny Example
A common setup is 5-way 1-shot or 5-way 5-shot episodes sampled from the test classes.

## Definition
mini-ImageNet contains 100 classes (typically split into 64 train / 16 val / 20 test) with 84x84 images.

## Math Form (if needed)
Episode accuracy is averaged over many sampled tasks to reduce variance.

## Key Points
1. Canonical benchmark in FSL literature.
2. Supports direct comparison across methods.
3. Sensitive to implementation details and evaluation protocol.

## How This Paper Uses It
- [[IBFS]]: Reports 5-way 1-shot/5-shot results to validate few-shot architecture quality.

## Representative Papers
- Vinyals et al. (2016): Popularized mini-ImageNet in matching-network style evaluation.
- [[IBFS]]: Uses mini-ImageNet for FSL benchmarking.

## Related Concepts
- [[Few-shot Learning]]
- [[tiered-ImageNet]]
