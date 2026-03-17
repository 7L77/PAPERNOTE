---
type: concept
language: zh-CN
source_concept_note: "[[Information Directed Sampling]]"
aliases: [IDS, 信息导向采样]
---

# Information Directed Sampling 中文条目

## 一句话直觉

IDS 的核心思想是：每次选动作时，不只看“当前看起来多好”，还看“这次查询能带来多少有价值信息”。

## 它为什么重要

当一次查询很贵时，理想策略应同时兼顾短期收益和长期认知提升，避免把预算浪费在信息增益很低的点上。

## 一个小例子

两个候选权重预测分数差不多时，IDS 会偏向那个能更快减少“谁更优”不确定性的候选，而不只是看均值略高者。

## 更正式的定义

IDS 在序列决策中最小化“信息比率”，权衡两件事：
- 期望即时遗憾（regret）；
- 关于最优动作的信息增益。

## 数学形式（如有必要）

常见信息比率形式：
\[
\Psi_t(a)=\frac{\Delta_t(a)^2}{g_t(a)}
\]

- \(\Delta_t(a)\): 选择动作 \(a\) 的期望遗憾。
- \(g_t(a)\): 动作 \(a\) 带来的信息增益。

每轮选择使 \(\Psi_t(a)\) 最小的动作。

## 核心要点

1. IDS 是“信息效率驱动”的探索-利用策略。
2. 在部分反馈问题中常用于建立更好的 regret 理论。
3. 与 UCB 同属 BO/bandit 思路，但决策准则不同。

## 这篇论文里怎么用
- [[RoBoT]]: 理论部分讨论 IDS 条件来支撑 BO 探索阶段的有界 regret 分析。

## 代表工作

- [[RoBoT]]: 在理论框架里引用 IDS 相关假设与结论。

## 相关概念

- [[Bayesian Optimization]]
- [[Partial Monitoring]]
