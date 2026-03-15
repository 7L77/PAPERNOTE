---
type: concept
language: zh-CN
source_concept_note: "[[Confidence Learning]]"
aliases: [置信学习, Confidence Learning]
---

# Confidence Learning 中文条目

## 一句话直觉
Confidence Learning 不只学习“参数该取什么值”，还学习“对这个值有多确定”。

## 它为什么重要
在搜索空间大、噪声高的优化问题里，只看均值容易过拟合到不稳定选择；加入置信度可提高最终离散化稳定性。

## 一个小例子
两个算子平均分几乎一样，但其中一个方差更大。置信学习会倾向选择方差更小的候选，从而减少搜索-采样偏差。

## 更正式的定义
置信学习是指：在参数学习中同时建模不确定性（如方差、置信区间、后验分布宽度），并把它用于约束、采样或决策。

## 数学形式（如有必要）
常见形式是概率约束，例如
`Pr(metric <= threshold) >= eta`，
把“值”和“置信度”同时放进优化目标。

## 核心要点
1. 把“值好坏”和“值是否可靠”分开建模。
2. 有助于平衡探索与利用。
3. 常通过分布参数（均值/方差）而非点估计实现。

## 这篇论文里怎么用
- [[RACL]]: 将架构参数建模为对数正态分布，并通过网络 Lipschitz 上界的概率约束实现置信驱动采样。

## 代表工作
- 不确定性建模、贝叶斯优化和 uncertainty-aware NAS 都采用了类似思想。

## 相关概念
- [[Log-normal Distribution]]
- [[Lipschitz Constant]]
- [[Differentiable Architecture Search]]
