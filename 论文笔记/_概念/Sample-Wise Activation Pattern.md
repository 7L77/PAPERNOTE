---
type: concept
aliases: [SWAP Pattern, Sample-wise Pattern]
---

# Sample-Wise Activation Pattern

## Intuition
Instead of looking at one sample's all-neuron activation code, this concept looks at one neuron's activation behavior across many samples.

## Why It Matters
In NAS scoring, this representation provides a much larger pattern space, so candidate architectures become easier to distinguish.

## Tiny Example
With batch size 4, a neuron may activate as `[1, 0, 1, 1]`. Another neuron may be `[0, 0, 1, 0]`. Counting unique such vectors across neurons yields a discrimination score.

## Definition
Given network \(N\), parameters \(\theta\), and \(S\) samples, sample-wise activation patterns are binary vectors built as \(\mathbf{1}(p_s^{(v)})_{s=1}^{S}\) for each intermediate activation index \(v\). The set cardinality is used by SWAP-Score.

## Key Points
1. Pattern vectors are indexed by neuron/intermediate value, not by sample.
2. The upper bound is linked to number of intermediate activations \(V\), often much larger than \(S\).
3. Unique-pattern count serves as an expressivity proxy.

## How This Paper Uses It
- [[SWAP-NAS]]: Defines SWAP-Score as the cardinality of sample-wise activation pattern set.

## Representative Papers
- [[SWAP-NAS]]: Introduces sample-wise activation patterns for training-free NAS scoring.

## Related Concepts
- [[Network Expressivity]]
- [[Zero-Cost Proxy]]

