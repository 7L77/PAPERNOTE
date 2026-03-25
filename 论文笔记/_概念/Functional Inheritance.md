---
type: concept
aliases: [Knowledge Inheritance in Pruning, Functional Preservation]
---

# Functional Inheritance

## Intuition
After pruning, a model may still "inherit" useful behavior from its pretrained parent if its optimization dynamics and representational pathways are not severely broken.

## Why It Matters
Compression for LLMs usually depends on post-pruning recovery, so selecting architectures with stronger inheritance can reduce recovery cost and improve final quality.

## Tiny Example
Two pruned models have equal parameter counts; the one whose gradients align better with the base model often recovers faster during continued pretraining.

## Definition
Functional inheritance is the extent to which a compressed/pruned model preserves the pretrained model's functional state, enabling effective recovery under limited retraining.

## Key Points
1. It emphasizes recoverability, not only immediate post-pruning accuracy.
2. It depends on global structure, not just local weight saliency.
3. It can be approximated by zero-shot proxies (for example gradient-trace alignment).

## How This Paper Uses It
- [[TraceNAS]] explicitly defines its search objective around functional inheritance and uses `Phi` as a proxy signal.

## Representative Papers
- [[TraceNAS]]: Uses gradient-trace alignment as a practical inheritance metric for LLM pruning.

## Related Concepts
- [[Gradient Trace Correlation]]
- [[Training-free NAS]]
- [[Structured Pruning]]
