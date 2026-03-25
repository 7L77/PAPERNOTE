---
type: concept
aliases: [Problem-Suggestion-Outcome Triple, Failure-Aware Triple]
---

# Diagnostic Triple

## Intuition
A Diagnostic Triple is a three-part record: what went wrong, what fix was suggested, and what happened after applying it.

## Why It Matters
Scalar scores alone hide the reason behind failure. Triple records preserve causality and help the model avoid repeating ineffective edits.

## Tiny Example
`(problem=shape mismatch, suggestion=add adaptive pooling, outcome=passes validation but no accuracy gain)`.

## Definition
A structured tuple
\[
(problem_i,\ suggestion_i,\ outcome_i)
\]
used as a unit feedback entry in iterative optimization.

## Key Points
1. Encodes both diagnosis and intervention, not just final score.
2. Makes failure trajectories reusable as training signal for prompt refinement.
3. Improves interpretability of iterative LLM search logs.

## How This Paper Uses It
- [[Iterative LLM-Based NAS with Feedback Memory]]: Stores each iteration in triple form and feeds recent triples back into Prompt Improver.

## Representative Papers
- [[Iterative LLM-Based NAS with Feedback Memory]]: Formalizes the triple in Eq. (3) for NAS feedback learning.

## Related Concepts
- [[Historical Feedback Memory]]
- [[LLM Reflection]]
- [[One-Epoch Proxy Evaluation]]
