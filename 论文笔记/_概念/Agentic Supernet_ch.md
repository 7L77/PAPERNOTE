---
type: concept
language: zh-CN
aliases: [Agentic Architecture Supernet_ch]
---

# Agentic Supernet

## Intuition

它的直觉是：不要给所有输入共用一个固定多智能体工作流，而是把很多可能的工作流都保留在一个概率化结构里，针对不同 query 再动态挑选。

## Why It Matters

它把 supernet 在 NAS 里的思想迁到 agent workflow 上，让系统既能保持搜索空间的丰富性，又能按输入难度分配推理资源。

## Tiny Example

一个简单算术题可能只激活 `Generate` 后立刻早停；一个复杂工具调用任务则可能激活多层 operator 再输出。

## Definition

Agentic supernet 是一个分层的工作流分布模型，层内保存候选 agentic operator 的激活概率；每次采样得到的是 query-specific workflow，而不是全局唯一解。

## Math Form (if needed)

在 MaAS 中，`A = {pi, O}`，其中 `pi_l(O)` 表示第 `l` 层选择 operator `O` 的条件概率。

## Key Points

1. 它优化的是“工作流分布”，不是“单个最终工作流”。
2. 它天然支持 query-dependent routing 和 early stopping。
3. 它特别适合同时关心效果和成本的 LLM-agent 系统。

## How This Paper Uses It

- [[MaAS]]: 用 agentic supernet 作为核心搜索对象，为每个 query 采样一个定制 workflow。

## Representative Papers

- [[MaAS]]: 在多智能体工作流搜索中首次系统性提出这一概念。

## Related Concepts

- [[Agentic Operator]]
- [[Early Exit]]
- [[Textual Gradient]]

