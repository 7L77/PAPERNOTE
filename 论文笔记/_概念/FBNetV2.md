---
type: concept
aliases: [FBNet V2, Hardware-aware Differentiable NAS]
---

# FBNetV2

## Intuition

FBNetV2 is a hardware-aware NAS framework that optimizes architecture choices with differentiable latency/efficiency objectives.

## Why It Matters

It provides a practical search recipe for mobile-efficient models, and many later methods reuse its differentiable search machinery.

## Tiny Example

Each block has candidate channel/operator options with soft architecture weights, and the objective includes task loss + efficiency term.

## Definition

A differentiable supernet search approach focused on direct hardware efficiency optimization (e.g., latency/FLOPs proxies) alongside accuracy.

## Math Form (if needed)

General pattern:
`L_total = L_task + lambda * L_efficiency`,
with differentiable architecture parameters.

## Key Points

1. Efficiency is optimized during search, not only after.
2. Uses soft architecture choices that can be discretized later.
3. Well-suited for mobile/edge deployment.

## How This Paper Uses It

- [[RNAS-CL]]: Reuses FBNetV2-style channel-search mechanism and latency-aware objective design.

## Representative Papers

- FBNetV2 (Wan et al., 2020): Differentiable neural architecture search for spatial/channel dimensions.

## Related Concepts

- [[Neural Architecture Search]]
- [[Gumbel-Softmax]]
