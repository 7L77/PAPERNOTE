---
type: concept
aliases: [Reflective Feedback in LLMs, LLM Self-Reflection]
---

# LLM Reflection

## Intuition
LLM reflection is a loop where the model inspects previous output quality (and errors) and then generates explicit suggestions to improve the next output.

## Why It Matters
It turns one-shot generation into iterative improvement, which is especially useful when outputs must satisfy structural constraints, like architecture strings in NAS.

## Tiny Example
If a generated architecture violates `MAX_LAYERS`, reflection adds a hint like "reduce layer count or simplify blocks" before the next mutation.

## Definition
LLM reflection is a feedback mechanism that conditions future generation on prior outcomes (scores, failures, diagnostics) to improve validity and performance.

## Key Points
1. Reflection can reduce invalid outputs in constrained generation tasks.
2. Reflection improves search by converting failures into actionable guidance.
3. Reflection quality depends on what signals are fed back (score, exception, constraints).

## How This Paper Uses It
- [[RZ-NAS]]: Uses internal prompt reflection instructions and external iteration-level feedback based on mutation score and exceptions.

## Representative Papers
- [[RZ-NAS]]: Reflection-guided architecture mutation in zero-cost NAS.
- [[Reflexion]]: Generate-evaluate-reflect loop for LLM agents.

## Related Concepts
- [[LLM-guided Search]]
- [[In-context Learning]]
- [[Evolutionary Neural Architecture Search]]
