---
type: concept
aliases: [Structured Model Pruning, Architecture-level Pruning]
---

# Structured Pruning

## Intuition
Structured pruning removes whole architectural units (for example blocks, heads, or channels), not just individual weights, so the pruned model is directly smaller and faster at runtime.

## Why It Matters
Unlike unstructured sparsity, structured pruning usually maps better to real hardware acceleration because model topology is physically simplified.

## Tiny Example
In a transformer, dropping several complete MLP channels and one full block reduces both parameter count and inference FLOPs without needing sparse kernels.

## Definition
Structured pruning is a compression strategy that removes pre-defined groups of parameters with architectural meaning, such as layers, attention heads, or neuron channels.

## Key Points
1. It changes network topology, not only weight values.
2. It typically gives stronger practical speedups than unstructured sparsity.
3. It can cause larger functional disruption, so architecture-aware scoring is important.

## How This Paper Uses It
- [[TraceNAS]] formulates LLM structured pruning as a joint depth-width search problem and scores candidates by gradient-trace alignment.

## Representative Papers
- [[TraceNAS]]: Uses training-free NAS to find non-uniform structured-pruned LLMs.
- [[LLM-Pruner]]: Early structured pruning framework tailored for LLM compression.

## Related Concepts
- [[Channel Pruning]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
