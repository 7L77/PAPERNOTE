---
type: concept
aliases: [LoRA Adapter, Low-rank Update]
---

# Low-Rank Adapter

## Intuition
Instead of updating all model weights, we inject small trainable low-rank matrices into selected layers to adapt a large model cheaply.

## Why It Matters
It drastically reduces trainable parameters and memory cost, making LLM adaptation practical.

## Tiny Example
A full weight matrix update may need millions of parameters, while a rank-8 adapter uses two small matrices whose product approximates the update.

## Definition
A low-rank adapter parameterizes weight change as \(\Delta W = BA\), where \(A\) and \(B\) are low-rank factors with rank \(r \ll d\).

## Math Form (if needed)
\[
\Delta W = BA
\]
- \(W\): original weight matrix
- \(\Delta W\): learned update
- \(r\): adapter rank controlling capacity and cost

## Key Points
1. Rank is the central capacity-efficiency knob.
2. Different layers may need different ranks.
3. It is a core building block in PEFT methods.

## How This Paper Uses It
- [[LLaMA-NAS]]: Searches layer-wise rank configurations instead of fixing a single rank globally.

## Representative Papers
- [[LLaMA-NAS]]: Uses mixed-rank low-rank adapters in a super-network.

## Related Concepts
- [[Parameter-Efficient Fine-Tuning]]
- [[Mixed-Rank Adapter]]
