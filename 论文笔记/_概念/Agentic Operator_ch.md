---
type: concept
language: zh-CN
aliases: [Operator for Agentic Workflow_ch]
---

# Agentic Operator

## Intuition

Agentic operator 可以理解成“可复用的 agent 工作流积木”。它不是单次 LLM 调用，而是可能包含 prompt、多次模型调用、tool 使用和控制逻辑的一段复合流程。

## Why It Matters

如果要搜索 multi-agent workflow，就必须先把 workflow 拆成可组合的基本单元；agentic operator 正是这个最小单元。

## Tiny Example

CoT、Debate、ReAct、Self-Refine、Early Exit 都可以看成 agentic operator，因为它们都描述了一种可复用的推理或交互模式。

## Definition

在 MaAS 中，agentic operator 被定义为由多个 LLM 实例、prompt 和 tools 组成的复合 LLM-agent 调用过程。

## Math Form (if needed)

论文写成 `O = {{M_i}_{i=1}^m, P, {T_i}_{i=1}^n}`，其中 `M_i` 是模型实例，`P` 是 prompt，`T_i` 是工具。

## Key Points

1. 它是 agentic supernet 里的基本搜索单元。
2. 多个 operator 可以跨层组合成 workflow DAG。
3. operator 自身也能通过 textual gradient 被改进。

## How This Paper Uses It

- [[MaAS]]: 通过 operator 库定义整个 workflow 搜索空间。

## Representative Papers

- [[MaAS]]: 把 agentic operator 明确形式化为搜索原子。

## Related Concepts

- [[Agentic Supernet]]
- [[Textual Gradient]]
- [[Chain-of-Thought Prompting]]

