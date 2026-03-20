---
type: concept
aliases: [Early Stop Operator]
---

# Early Exit

## Intuition

Some inputs do not need the full depth of a reasoning system. Early exit lets the system stop once enough computation has already been used.

## Why It Matters

Without early exit, every query pays for the deepest workflow. That wastes tokens and API calls on easy inputs.

## Tiny Example

A query like "2 + 2" should not trigger multi-round debate, tool use, and self-refinement. An early-exit operator allows the workflow to stop after a shallow layer.

## Definition

Early exit is a routing decision or operator that terminates deeper workflow sampling when the current partial workflow is already sufficient for the query.

## Math Form (if needed)

In MaAS, the controller stops sampling deeper layers when `O_exit` is selected, making workflow depth query-dependent.

## Key Points

1. It makes computation adaptive rather than fixed-depth.
2. It is one of the main reasons MaAS saves inference cost.
3. It matters most when query difficulty is highly variable.

## How This Paper Uses It

- [[MaAS]]: introduces an explicit early-exit operator inside the supernet so simple queries can terminate early.

## Representative Papers

- [[MaAS]]: uses early exit as a core mechanism for cost-aware dynamic routing.

## Related Concepts

- [[Agentic Supernet]]
- [[Agentic Operator]]
- [[Textual Gradient]]

