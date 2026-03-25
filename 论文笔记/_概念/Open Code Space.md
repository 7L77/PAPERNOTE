---
type: concept
aliases: [Unconstrained Code Space, Program-Level Search Space]
---

# Open Code Space

## Intuition
Open Code Space means searching architectures by generating executable code directly, rather than selecting from a fixed menu of pre-defined cells or operators.

## Why It Matters
It expands design flexibility and can discover structures not expressible in rigid cell-based encodings.

## Tiny Example
A fixed NAS cell space may allow only pre-listed edges and ops, while open code space can introduce a custom branching module or non-standard block layout.

## Definition
A search space where candidate architectures are represented as executable programs, with minimal predefined structural constraints beyond runtime validity.

## Key Points
1. Higher expressiveness than discrete pre-indexed cell spaces.
2. Usually harder to optimize due to larger and noisier search manifold.
3. Needs strong validation safeguards because invalid code is common.

## How This Paper Uses It
- [[Iterative LLM-Based NAS with Feedback Memory]]: Uses LLM-generated PyTorch programs as direct architecture candidates in a closed-loop search.

## Representative Papers
- [[Iterative LLM-Based NAS with Feedback Memory]]: Positions itself explicitly against constrained cell-space NAS formulations.

## Related Concepts
- [[Cell-based Search Space]]
- [[LLM-guided Search]]
- [[Neural Architecture Search]]
