---
type: concept
aliases: [PEFT, Efficient Fine-Tuning]
---

# Parameter-Efficient Fine-Tuning

## Intuition
PEFT adapts large pretrained models by training only a tiny subset of extra or selected parameters, while keeping the backbone mostly frozen.

## Why It Matters
It enables rapid adaptation of large models on limited compute and memory budgets.

## Tiny Example
Instead of updating all billions of model parameters, you train only adapters or prompts that are often less than 1% of total parameters.

## Definition
PEFT is a family of fine-tuning strategies that reduce trainable parameter count and optimizer/memory overhead while preserving downstream quality.

## Key Points
1. PEFT targets cost-efficiency, not only raw accuracy.
2. Adapter design and rank selection strongly affect quality.
3. NAS can be used to automate PEFT structure selection.

## How This Paper Uses It
- [[LLaMA-NAS]]: Treats adapter architecture search as a PEFT optimization problem.

## Representative Papers
- [[LLaMA-NAS]]: Uses NAS to improve PEFT adapter configuration.

## Related Concepts
- [[Low-Rank Adapter]]
- [[Neural Architecture Search]]
