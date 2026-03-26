---
type: concept
aliases: [FA, Random Feedback Alignment]
---

# Feedback Alignment

## Intuition
Feedback Alignment (FA) replaces exact backpropagation feedback with fixed random feedback paths, while still allowing useful learning to emerge.

## Why It Matters
It relaxes the biologically implausible requirement that backward weights must be the exact transpose of forward weights.

## Tiny Example
In a two-layer MLP, BP sends gradient through `W2^T`; FA instead uses a fixed random matrix `B2` to transmit error to the hidden layer.

## Definition
FA is a credit-assignment rule where hidden-layer updates are driven by random fixed feedback matrices rather than exact gradient backpropagation through transposed forward weights.

## Key Points
1. FA is more biologically plausible than strict BP symmetry.
2. It can work surprisingly well, though often below full BP accuracy.
3. Variants (uSF/brSF/frSF) modify magnitude/sign constraints on feedback.

## How This Paper Uses It
- [[BioNAS]] includes FA as one searchable per-layer learning rule, and mixes it with other rules during NAS.

## Representative Papers
- [[Feedback Alignment]] (classic line of work; listed as [31] in BioNAS).
- [[Benchmarking the accuracy and robustness of biologically inspired neural networks]] (reported as [47] in BioNAS context).

## Related Concepts
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Hebbian Learning]]
- [[Predictive Coding]]

