---
type: concept
aliases: [FSL, N-way K-shot Learning]
---

# Few-shot Learning

## Intuition
Few-shot learning aims to learn new tasks from very few labeled examples.

## Why It Matters
It addresses data-scarce scenarios where collecting many labels per class is expensive or impossible.

## Tiny Example
In 5-way 1-shot classification, the model must classify among 5 classes with only 1 labeled example per class.

## Definition
FSL usually follows episodic evaluation with support/query sets under N-way K-shot settings.

## Math Form (if needed)
A task episode contains `D_support` and `D_query`; performance is evaluated on `D_query` after adapting on `D_support`.

## Key Points
1. Generalization with tiny supervision is central.
2. Meta-learning and metric learning are common paradigms.
3. Benchmarks often include mini-ImageNet and tiered-ImageNet.

## How This Paper Uses It
- [[IBFS]]: Targets architecture search specifically for few-shot tasks and reports 5-way 1/5-shot results.

## Representative Papers
- Finn et al. (2017): MAML for few-shot learning.
- [[IBFS]]: Few-shot-friendly training-free NAS.

## Related Concepts
- [[Model-Agnostic Meta-Learning]]
- [[mini-ImageNet]]
- [[tiered-ImageNet]]
