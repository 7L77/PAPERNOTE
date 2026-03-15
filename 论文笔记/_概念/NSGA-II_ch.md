---
type: concept
language: zh-CN
source_concept_note: "[[NSGA-II]]"
aliases: [非支配排序遗传算法II, NSGA-II]
---

# NSGA-II 中文条目

## 一句话直觉
NSGA-II 是专门做多目标优化的进化算法，它不会把多个目标硬压成一个分数，而是保留一组互不支配的候选解。

## 它为什么重要
在“精度 vs 参数量”这类冲突目标下，NSGA-II 能直接输出可选 Pareto 解集，方便按预算选型。

## 一个小例子
一个模型更准但更大，另一个更小但略差。如果彼此都没有完全碾压对方，NSGA-II 会把两者都保留。

## 更正式的定义
NSGA-II 通过非支配排序与拥挤度距离维持解集质量和多样性，逐代逼近 Pareto 前沿。

## 核心要点
1. 原生支持多目标，不必先做人为加权。
2. 同时考虑“优劣”和“多样性”。
3. 输出是一组候选而不是单解。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 用 NSGA-II 在 adapter 搜索空间里同时优化任务性能和参数规模。

## 代表工作
- [[LLaMA-NAS]]: 将 NSGA-II 用于 LLM adapter 的多目标 NAS。

## 相关概念
- [[Pareto Front]]
- [[Neural Architecture Search]]
