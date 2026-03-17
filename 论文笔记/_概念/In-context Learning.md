---
type: concept
aliases: [In-Context Example Learning, ICL]
---

# In-context Learning

## Intuition
Instead of updating model weights, we give examples in the prompt so the model infers the desired behavior from context.

## Why It Matters
For structured generation tasks, good examples can stabilize format, reduce syntax errors, and encode task-specific heuristics without retraining.

## Tiny Example
Show one architecture mutation JSON pair in the prompt; the model then follows the same JSON schema for a new architecture.

## Definition
In-context learning is the ability of a language model to adapt its output behavior from demonstrations and instructions provided in the current input context.

## Key Points
1. Works as a lightweight adaptation mechanism.
2. Strongly affects output format consistency and task success.
3. Sensitive to example quality and alignment with current task.

## How This Paper Uses It
- [[RZ-NAS]]: Includes mutation examples in prompt template; ablation shows removing this part increases exceptions and lowers performance.

## Representative Papers
- [[RZ-NAS]]: Demonstrates practical impact in LLM-guided NAS.
- [[Language Models are Few-Shot Learners]]: Foundational ICL evidence.

## Related Concepts
- [[LLM Reflection]]
- [[Prompt Engineering]]
- [[Chain-of-Thought Prompting]]
