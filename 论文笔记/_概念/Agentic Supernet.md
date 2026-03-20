---
type: concept
aliases: [Agentic Architecture Supernet]
---

# Agentic Supernet

## Intuition

Instead of choosing one fixed multi-agent workflow for all inputs, an agentic supernet keeps many possible workflows "alive" inside one probabilistic structure and lets the system pick different ones for different queries.

## Why It Matters

It gives agent systems the same kind of flexibility that supernets gave neural architecture search: you do not commit early to one architecture, and you can adapt computation to the input.

## Tiny Example

For a simple arithmetic query, the supernet may activate only `Generate` and then exit. For a harder tool-use query, it may activate several operators across multiple layers before stopping.

## Definition

An agentic supernet is a layered probabilistic distribution over candidate agentic operators and their compositions. Sampling from it yields a query-specific workflow rather than a single globally fixed workflow.

## Math Form (if needed)

In MaAS, the supernet is written as `A = {pi, O}`, where `pi_l(O)` denotes the probability of choosing operator `O` at layer `l`, conditioned on earlier layers.

## Key Points

1. It models a distribution over workflows, not one final workflow.
2. It supports query-dependent routing and early stopping.
3. It is useful when both accuracy and inference cost matter.

## How This Paper Uses It

- [[MaAS]]: uses the agentic supernet as the main search object and samples a custom workflow per query.

## Representative Papers

- [[MaAS]]: introduces the term for multi-agent workflow search.

## Related Concepts

- [[Agentic Operator]]
- [[Early Exit]]
- [[Textual Gradient]]

