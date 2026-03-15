---
type: concept
language: zh-CN
source_concept_note: "[[Multi-Armed Bandit]]"
aliases: [多臂老虎机, Multi-Armed Bandit]
---

# Multi-Armed Bandit 中文条目

## 一句话直觉
多臂老虎机问题研究的是：在多个不确定选项之间，如何平衡“继续试新选项”和“利用已知好选项”。

## 它为什么重要
它是探索-利用权衡的经典数学模型，广泛用于推荐、广告、超参搜索和 NAS 策略设计。

## 一个小例子
给用户推荐内容时，系统既要推历史上点击率高的内容，也要偶尔试新内容，避免长期陷入局部最优。

## 更正式的定义
在每一轮选择一个臂并观察随机回报，目标是在有限轮次内最大化累计回报（或最小化 regret）。

## 数学形式（如有必要）
\[
R_T = \sum_{t=1}^T (\mu^\* - \mu_{a_t})
\]
其中 `mu*` 是最优臂期望回报，`mu_{a_t}` 是第 `t` 轮所选臂期望回报。

## 核心要点
1. 反馈是部分可观测的（只看到被选臂的回报）。
2. 不探索就容易错过潜在更优臂。
3. UCB/Thompson Sampling 是常见策略。

## 这篇论文里怎么用
- [[ABanditNAS]]: 把 NAS 的边-操作选择建模成巨大臂数 bandit，并设计 anti-bandit 版本。

## 代表工作
- Auer et al. (2002): UCB 经典分析。
- Kocsis and Szepesvari (2006): UCB 在树搜索中的应用。

## 相关概念
- [[Upper Confidence Bound (UCB)]]
- [[Lower Confidence Bound (LCB)]]
- [[Neural Architecture Search]]

