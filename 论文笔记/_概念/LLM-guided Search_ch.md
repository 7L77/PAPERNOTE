---
type: concept
language: zh-CN
source_concept_note: "[[LLM-guided Search]]"
aliases: [LLM引导搜索, 大模型辅助搜索]
---

# LLM-guided Search 中文条目

## 一句话直觉
让大语言模型参与“生成候选解”这一步，用它的先验知识替代部分随机或手工规则。

## 它为什么重要
在离散组合搜索里，随机探索效率低；LLM 可能提供更有结构性的候选，减少无效尝试。

## 一个小例子
给 LLM 两个父代架构和历史性能，它生成一个“保留优点、规避弱点”的新架构作为后代。

## 更正式的定义
LLM-guided Search 是指在迭代优化流程中，使用 LLM 输出直接驱动候选生成、编辑或排序的搜索范式。

## 核心要点
1. prompt 设计和模型能力决定效果。
2. 对结构化离散空间常有探索效率优势。
3. 会引入额外调用成本和结果波动。

## 这篇论文里怎么用
- [[LLMENAS]]: 将 LLM 作为进化交叉/变异算子的核心执行器。

## 代表工作
- [[LLMENAS]]: LLM 引导进化 NAS。
- [[Large Language Models as Optimizers]]: 把 LLM 当作优化器的代表方向。

## 相关概念
- [[Evolutionary Neural Architecture Search]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]

