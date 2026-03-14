---
type: concept
language: zh-CN
source_concept_note: "[[Gumbel-Top-k Reparameterization]]"
aliases: [Gumbel-Top2 重参数化, Gumbel Top-k 采样]
---

# Gumbel-Top-k Reparameterization 中文条目

## 一句话直觉

Gumbel-Top-k 可以在“必须同时选 k 个离散项”的场景里做可微采样，是 Gumbel-Max（只选 1 个）的扩展。

## 它为什么重要

很多结构约束不是 top-1，而是“固定选 k 个”，比如每个节点保留 2 条入边。Gumbel-Top-k 可以直接处理这种约束。

## 一个小例子

一个节点有 4 条候选入边，要求保留 2 条。Gumbel-Top2 会给每条边的 `log p` 加噪声后取前 2 名，并用软松弛保持梯度可传。

## 更正式的定义

对每个候选 `i`，计算 `s_i = log p_i + g_i`（`g_i ~ Gumbel(0,1)`），按 `s_i` 排序取 top-k；训练时配合温度 softmax 做连续近似。

## 数学形式（如有必要）

\[
s_i = \log p_i + g_i,\quad g_i \sim \text{Gumbel}(0,1)
\]

按 `s_i` 取 top-k，温度参数控制软到硬的过渡。

## 核心要点

1. 从“选 1 个”推广到“选 k 个”。
2. 适合带基数约束（cardinality constraint）的结构采样。
3. 与 soft relaxation 结合后可用于梯度优化。

## 这篇论文里怎么用

- [[ROME]]: ROME-v2 用 Gumbel-Top2 保证每个中间节点恰好选两条入边。

## 代表工作

- [[ROME]]: 在拓扑采样中系统使用 Gumbel-Top2。
- [[GDAS]]: 使用 Gumbel 机制进行算子采样（top-1）。

## 相关概念

- [[Differentiable Architecture Search]]
- [[Topology Disentanglement]]

