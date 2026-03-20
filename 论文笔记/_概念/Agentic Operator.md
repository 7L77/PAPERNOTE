---
type: concept
aliases: [Operator for Agentic Workflow]
---

# Agentic Operator

## Intuition

An agentic operator is a reusable workflow primitive. It is more than a single LLM call: it can include prompts, multiple model calls, tools, and control logic.

## Why It Matters

If multi-agent workflows are the search target, we need modular building blocks. Agentic operators provide that modular unit.

## Tiny Example

`CoT`, `Debate`, `ReAct`, `Self-Refine`, and `Early Exit` can all be viewed as agentic operators because each defines a reusable pattern of reasoning or interaction.

## Definition

In MaAS, an agentic operator is a composite LLM-agent invocation process that may contain multiple LLM instances, prompts, and tools.

## Math Form (if needed)

The paper writes an operator as `O = {{M_i}_{i=1}^m, P, {T_i}_{i=1}^n}`, where `M_i` are model instances, `P` is a prompt, and `T_i` are tools.

## Key Points

1. It is the basic search unit inside the agentic supernet.
2. Operators can be chained across layers to form a workflow DAG.
3. Operators can themselves be improved by textual gradient updates.

## How This Paper Uses It

- [[MaAS]]: defines the workflow search space through a library of agentic operators.

## Representative Papers

- [[MaAS]]: formalizes agentic operators as the atomic unit of workflow search.

## Related Concepts

- [[Agentic Supernet]]
- [[Textual Gradient]]
- [[Chain-of-Thought Prompting]]

