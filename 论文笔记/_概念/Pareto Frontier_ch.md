---
type: concept
language: zh-CN
source_concept_note: "[[Pareto Frontier]]"
aliases: ["帕累托前沿", "Pareto Frontier"]
---

# Pareto Frontier 中文条目

## 一句话直觉

当我们同时看精度和延迟时，通常没有唯一最优；Pareto Frontier 就是那一组“再提一个指标就必然伤另一个指标”的最优折中点。

## 它为什么重要

Hardware-aware NAS 本质上是多目标问题，不看 Pareto 前沿，就很容易只盯着某一个指标做出误判。

## 一个小例子

如果模型 A 比模型 B 更准，而且一点也不更慢，那 B 就被 A 支配，不应该出现在 Pareto 前沿上。

## 更正式的定义

Pareto Frontier 是在多个竞争目标下不被其他解严格支配的候选解集合。

## 核心要点

1. 它是分析精度-效率折中的标准语言。
2. 约束越宽松，真正靠近前沿的点往往越依赖高精度区域排序质量。
3. 一个 proxy 即使全局相关性还行，也可能恢复不出好的 Pareto 前沿。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 用 energy 与 latency 约束下的真实 Pareto front 来检验 proxy 找到的候选质量。

## 代表工作

- [[Zero-shot NAS Survey]]: 讨论硬件约束场景中的 Pareto 质量。
- [[HW-NAS-Bench]]: 常用于研究硬件代价下的 Pareto tradeoff。

## 相关概念

- [[Hardware-aware NAS]]
- [[Hardware Performance Model]]

