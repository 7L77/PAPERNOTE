---
type: concept
language: zh-CN
source_concept_note: "[[In-context Learning]]"
aliases: [上下文学习, ICL]
---

# In-context Learning 中文条目

## 一句话直觉
不改模型参数，只靠提示词里的示例让模型“当场学会”任务格式和策略。

## 为什么重要
在结构化输出任务里，ICL 能明显提升格式稳定性，减少语法错误，还能传递任务偏好。

## 小例子
提示词先给一个 JSON 变异示例，再给新架构输入，模型通常会沿用同样的 JSON 输出格式。

## 更正式定义
In-context Learning 指模型根据当前输入中的指令和示例，自适应调整输出行为的能力，而不进行参数更新。

## 核心要点
1. 这是“零训练成本”的快速适配手段。
2. 示例质量会直接影响效果上限。
3. 对复杂任务，ICL 常与反思机制联合使用。

## 这篇论文怎么用
- [[RZ-NAS]]：prompt 中包含 in-context mutation 示例；去掉该模块会导致异常率上升、性能下降。

## 代表工作
- [[RZ-NAS]]
- [[Language Models are Few-Shot Learners]]

## 相关概念
- [[LLM Reflection]]
- [[Prompt Engineering]]
- [[Chain-of-Thought Prompting]]
