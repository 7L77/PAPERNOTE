---
type: concept
language: zh-CN
source_concept_note: "[[Differentiable Architecture Search]]"
aliases: [可微架构搜索, DARTS-style NAS]
---

# Differentiable Architecture Search 中文条目

## 一句话直觉

可微架构搜索把“选哪种网络结构”变成可求导的连续参数学习问题，从而能用梯度直接搜索架构。

## 它为什么重要

相比 RL/进化式 NAS，它显著降低了搜索算力成本，让 NAS 能在常规算力预算下落地。

## 一个小例子

一条边可选 `3x3 conv` 或 `skip`。可微 NAS 不直接二选一，而是先给两者分配可学习权重，训练后再离散化选最优项。

## 更正式的定义

Differentiable Architecture Search 通过 softmax/Gumbel-softmax 等连续松弛方式参数化离散结构决策，并与网络权重联合或双层优化。

## 数学形式（如有必要）

\[
\bar{o}(x) = \sum_{o \in \mathcal{O}} \text{softmax}(\alpha)_o \cdot o(x)
\]

其中 `alpha` 是架构参数，`\mathcal{O}` 是候选算子集合。

## 核心要点

1. 把组合搜索问题转为梯度优化问题。
2. 常用双层优化：训练集更新权重，验证集更新架构参数。
3. 连续松弛与最终离散结构之间可能存在不一致，导致不稳定。

## 这篇论文里怎么用

- [[ROME]]: 在单路径可微 NAS 框架上，进一步通过 TD+GA 修复 collapse 与不稳定问题。

## 代表工作

- [[DARTS]]: 可微 NAS 的经典方法。
- [[GDAS]]: 基于 Gumbel 的单路径可微 NAS。

## 相关概念

- [[Neural Architecture Search]]
- [[One-shot NAS]]

