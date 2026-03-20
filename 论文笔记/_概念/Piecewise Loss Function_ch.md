---
type: concept
language: zh-CN
source_concept_note: "[[Piecewise Loss Function]]"
aliases: [Piecewise Loss, Staged Loss Schedule]
---

# Piecewise Loss Function 中文条目

## 一句话直觉

Piecewise Loss Function 指“按阶段换损失函数”，而不是从头到尾固定一个 loss。

## 它为什么重要

在迭代 NAS 搜索中，样本规模和数据分布不断变化，单一 loss 往往无法全程最优。

## 一个小例子

前期样本少，用排序损失稳住相对顺序；后期样本多，切到 weighted loss 提升 top 架构命中率。

## 更正式的定义

通用形式：
\[
\mathcal{L}(t)=
\begin{cases}
\mathcal{L}_{warm}, & t \le t_{warm}\\
\mathcal{L}_{focus}, & t > t_{warm}
\end{cases}
\]

## 数学形式（如有必要）

- \(\mathcal{L}_{warm}\): 前期目标。
- \(\mathcal{L}_{focus}\): 后期目标。
- \(t_{warm}\): 切换阈值（可按迭代轮次或样本数定义）。

## 核心要点

1. 这是“目标函数调度”，不是学习率调度。
2. 适合多阶段优化目标不一致的问题。
3. 阈值和组合策略需要任务相关调参。

## 这篇论文里怎么用

- [[PWLNAS]]: 方法核心即分段损失，跨多个 benchmark 验证优于单一损失。

## 代表工作

- [[PWLNAS]]: 将分段 loss 用于 predictor-based NAS 并给出实证组合经验。

## 相关概念

- [[Pairwise Ranking Loss]]
- [[MAPE Loss]]
