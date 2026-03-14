---
type: concept
aliases: [LLM-guided Optimization, LLM-assisted Search]
---

# LLM-guided Search

## Intuition
Use a large language model as a search operator or policy prior to propose better candidates than random or handcrafted heuristics.

## Why It Matters
LLMs can encode broad structural priors and textual reasoning patterns, which may improve search quality in discrete combinational spaces.

## Tiny Example
Given two parent architectures and performance history, ask an LLM to generate a child architecture that preserves strong motifs and avoids known weak patterns.

## Definition
LLM-guided search is an optimization framework where LLM outputs directly influence candidate generation, editing, or ranking during iterative search.

## Key Points
1. Quality depends on prompt design and model capability.
2. Can improve exploration efficiency in structured search spaces.
3. Introduces an extra dependency on LLM serving cost and variance.

## How This Paper Uses It
- [[LLMENAS]]: Uses LLM-generated crossover and mutation operators as the core evolution mechanism.

## Representative Papers
- [[LLMENAS]]: LLM-guided evolutionary NAS.
- [[Large Language Models as Optimizers]]: LLM as iterative optimizer paradigm.

## Related Concepts
- [[Evolutionary Neural Architecture Search]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]

