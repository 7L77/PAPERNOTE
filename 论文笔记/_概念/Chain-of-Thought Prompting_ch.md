---
type: concept
language: zh-CN
source_concept_note: "[[Chain-of-Thought Prompting]]"
aliases: [CoT 提示, 思维链提示]
---

# Chain-of-Thought Prompting 中文条目

## 一句话直觉

先让模型“把思路说出来”，再给最终答案，通常比直接要答案更稳。

## 它为什么重要

在多步推理任务里，模型直接输出最终结果容易跳步或遗漏关键约束；CoT 能把复杂任务拆解成可控步骤。

## 一个小例子

让模型先解释“为什么这个 proxy 可能和最终精度相关”，再输出代码实现，往往比直接“写一个 proxy”得到更可靠的候选。

## 更正式的定义

Chain-of-Thought Prompting 指通过提示词显式诱导模型输出中间推理过程，再输出最终答案，以提升复杂任务的推理质量。

## 核心要点

1. 适合需要多步组合推理的任务。
2. 相比直接答案提示，通常更稳健。
3. 生成的中间 reasoning 可用于后续迭代优化与诊断。

## 这篇论文里怎么用

- [[APD]]: 将“naive prompt 缺少推理与反馈”作为问题根源，并通过 RL 闭环提升 proxy 生成质量。

## 代表工作

- [[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]: CoT 提示代表性工作。
- [[Large Language Models as Optimizers]]: 展示结构化推理在优化任务中的价值。

## 相关概念

- [[LLM-guided Search]]
- [[Actor-Critic Reinforcement Learning]]
- [[Zero-Cost Proxy]]

