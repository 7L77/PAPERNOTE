---
type: concept
language: zh-CN
source_concept_note: "[[Gradient Accumulation]]"
aliases: [梯度累积, 多样本梯度平均]
---

# Gradient Accumulation 中文条目

## 一句话直觉

梯度累积是在一次参数更新前，先收集多个子步骤的梯度再统一更新，用计算换稳定性。

## 它为什么重要

在随机采样很强的 NAS 里，单次采样梯度噪声大且不公平。多样本累积能让更新更稳、覆盖更均衡。

## 一个小例子

如果每轮只采 1 个子网，某些算子很少被训练。改为每轮采 `K=7` 个子网并累积梯度后，参数更新会更平衡。

## 更正式的定义

Gradient Accumulation 指在多个 micro-step（或多个采样子网）上先计算梯度，再将这些梯度求和或求均值后做一次优化器更新。

## 数学形式（如有必要）

\[
\hat{g} = \frac{1}{K}\sum_{k=1}^{K} g_k,\quad Var(\hat{g})=\sigma^2/K
\]

其中 `g_k` 是第 `k` 个样本/子网的梯度估计。

## 核心要点

1. 降低随机梯度方差。
2. 提升对低频采样模块的训练公平性。
3. 通常增加每轮计算量，但换来更稳定的收敛。

## 这篇论文里怎么用

- [[ROME]]: 分别对架构参数（`alpha`,`beta`）和超网权重（`omega`）使用两段梯度累积。

## 代表工作

- [[ROME]]: 在单路径可微 NAS 中把梯度累积作为核心稳态机制。
- [[GDAS]]: 其单样本采样噪声问题促成了 ROME 的 GA 设计。

## 相关概念

- [[Differentiable Architecture Search]]
- [[One-shot NAS]]

