---
type: concept
aliases: [CoT Prompting, Reasoning Prompting]
---

# Chain-of-Thought Prompting

## Intuition

Instead of asking a model to output only the final answer, ask it to produce intermediate reasoning steps first. This often improves performance on multi-step tasks.

## Why It Matters

Complex tasks (planning, composition, algorithm design) often fail when a model jumps directly to output. Chain-of-thought encourages decomposition and can make generation more consistent.

## Tiny Example

For proxy discovery, a prompt can require:
1) explain why a metric should correlate with accuracy,
2) then provide executable code.
This tends to produce better candidate proxies than "just write code."

## Definition

Chain-of-thought prompting is a prompting strategy that elicits explicit intermediate reasoning tokens before a final response, typically to improve multi-step inference quality.

## Key Points

1. Best suited to tasks requiring compositional reasoning.
2. Often improves robustness versus direct-answer prompting.
3. Reasoning text can be used as searchable context for iterative refinement.

## How This Paper Uses It

- [[APD]]: Motivates using RL feedback to emulate a reasoning-improving loop beyond naive one-shot prompt generation.

## Representative Papers

- [[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]: Foundational CoT prompting paper.
- [[Large Language Models as Optimizers]]: Uses structured reasoning for iterative optimization behaviors.

## Related Concepts

- [[LLM-guided Search]]
- [[Actor-Critic Reinforcement Learning]]
- [[Zero-Cost Proxy]]

