---
type: concept
aliases: [Bounded Feedback History, Sliding Feedback Window]
---

# Historical Feedback Memory

## Intuition
Historical Feedback Memory is a compact notebook of recent attempts, where each attempt records what problem was found, what change was proposed, and what happened after the change.

## Why It Matters
Iterative LLM optimization can drift or repeat past mistakes. A bounded memory gives enough context to learn from recent failures without blowing up prompt length.

## Tiny Example
If the last two model edits both caused shape mismatch, the next prompt can explicitly avoid repeating those edits and prioritize stable output dimensions.

## Definition
A fixed-size history buffer that stores recent improvement attempts and outcomes, typically truncated to the latest `K` entries at each step.

## Math Form (if needed)
\[
H_t^{(K)}=\{(s_{t-K},a_{t-K}), \ldots, (s_{t-1},a_{t-1})\}
\]
Where `s_i` is the suggestion at step `i` and `a_i` is its observed outcome.

## Key Points
1. Keeps context length stable while preserving recent causally useful evidence.
2. Encourages learning from both success and failure, not only top scores.
3. Often works better than unbounded history in resource-limited settings.

## How This Paper Uses It
- [[Iterative LLM-Based NAS with Feedback Memory]]: Uses a sliding window of `K=5` attempts as the core iterative signal.

## Representative Papers
- [[Iterative LLM-Based NAS with Feedback Memory]]: Introduces the bounded memory design for code-level NAS loop control.

## Related Concepts
- [[Diagnostic Triple]]
- [[LLM-guided Search]]
- [[Neural Architecture Search]]
