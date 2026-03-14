---
type: concept
language: zh-CN
source_concept_note: "[[Evolutionary Neural Architecture Search]]"
aliases: [进化神经架构搜索, Evolutionary NAS]
---

# Evolutionary Neural Architecture Search 中文条目

## 一句话直觉
把网络结构当成“种群个体”，通过选择、交叉、变异迭代进化出更好的架构。

## 它为什么重要
进化方法天然适合离散搜索空间，不依赖可微假设，常用于复杂结构组合问题。

## 一个小例子
每一代保留表现好的架构，把两个父代结构拼接，再随机改一个操作，形成新架构并继续评估。

## 更正式的定义
Evolutionary NAS 是在架构搜索空间上进行种群优化的 NAS 范式，通过适应度驱动的进化循环来优化模型性能。

## 核心要点
1. 对离散决策友好。
2. 交叉/变异规则设计决定上限。
3. 若无快速评估机制，搜索成本会很高。

## 这篇论文里怎么用
- [[LLMENAS]]: 用 LLM 指导交叉与变异，替代传统手工规则。

## 代表工作
- [[AmoebaNet]]: 经典大规模进化 NAS。
- [[Regularized Evolution for Image Classifier Architecture Search]]: 老化进化策略。

## 相关概念
- [[Neural Architecture Search]]
- [[One-shot NAS]]
- [[LLM-guided Search]]

