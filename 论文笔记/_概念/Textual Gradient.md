---
type: concept
aliases: [Text Gradient]
---

# Textual Gradient

## Intuition

When part of a system is not differentiable, you can still ask an LLM to describe how that part should change. That natural-language update signal is a textual gradient.

## Why It Matters

Prompts, tool choices, and workflow nodes in agent systems are hard to optimize with ordinary backpropagation. Textual gradients give a practical workaround.

## Tiny Example

If a debate operator is unstable, a textual gradient might say: "lower the temperature" or "add a stronger critique prompt before voting."

## Definition

A textual gradient is an LLM-generated natural-language update signal that suggests how to modify prompts, temperatures, or operator structure based on observed task feedback.

## Math Form (if needed)

MaAS writes the operator-side gradient as `dL/dO = T_P union T_T union T_N`, where the text feedback targets prompt updates, temperature updates, and node-structure updates.

## Key Points

1. It is an optimization signal in words rather than numbers.
2. It is useful for non-differentiable parts of agent systems.
3. It complements numeric gradient estimation on the routing distribution.

## How This Paper Uses It

- [[MaAS]]: uses textual gradient to update prompts, temperatures, and operator node structure when direct gradients are unavailable.

## Representative Papers

- [[MaAS]]: integrates textual gradient into agentic workflow search.

## Related Concepts

- [[Agentic Supernet]]
- [[Agentic Operator]]
- [[Early Exit]]

