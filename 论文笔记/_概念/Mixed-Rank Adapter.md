---
type: concept
aliases: [Elastic Rank Adapter, Multi-rank Adapter]
---

# Mixed-Rank Adapter

## Intuition
A mixed-rank adapter allows multiple rank choices within one unified framework, so each layer can effectively choose different capacity.

## Why It Matters
Fixed-rank adapters can underfit some layers and over-parameterize others. Mixed-rank design enables finer efficiency-accuracy control.

## Tiny Example
Lower layers may use rank 4 while middle layers use rank 16. A mixed-rank scheme keeps these options searchable instead of forcing one rank everywhere.

## Definition
A mixed-rank adapter is an adapter design where rank choices are embedded in a super-network, enabling subnetwork extraction with different layer-wise rank configurations.

## Key Points
1. It decouples layer capacity from a single global rank.
2. It is naturally compatible with one-shot NAS.
3. It creates a richer search space for Pareto optimization.

## How This Paper Uses It
- [[LLaMA-NAS]]: Core structural unit of its super-network for adapter architecture search.

## Representative Papers
- [[LLaMA-NAS]]: Introduces mixed-rank adapters for LLM NAS.

## Related Concepts
- [[Super-network]]
- [[Low-Rank Adapter]]
