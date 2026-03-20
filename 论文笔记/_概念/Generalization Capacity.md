---
type: concept
aliases: ["Generalization", "Out-of-sample Performance"]
---

# Generalization Capacity

## Intuition

Generalization capacity is about whether a network that fits the seen data will also work on unseen data. It separates useful learning from mere memorization.

## Why It Matters

NAS cares about the final test performance, not just whether a model can optimize training loss. A proxy that ignores generalization may rank brittle networks too highly.

## Tiny Example

Two architectures may both fit a training subset well, but one transfers much better to validation data. The second architecture has stronger generalization capacity.

## Definition

Generalization capacity is the ability of a learned model or architecture to maintain performance on unseen samples drawn from the target data distribution or nearby distributions.

## Key Points

1. It is often the hardest property to estimate at initialization.
2. Many zero-shot proxies neglect it almost entirely.
3. A proxy that mixes trainability and generalization may be more useful than one that captures either alone.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: identifies poor coverage of generalization as a major weakness of current proxy design.

## Representative Papers

- [[Zero-shot NAS Survey]]: argues current proxies underrepresent this axis.
- [[ZiCo]]: discussed in the paper as a direction that may better capture generalization plus trainability.

## Related Concepts

- [[Expressive Capacity]]
- [[Trainability]]

