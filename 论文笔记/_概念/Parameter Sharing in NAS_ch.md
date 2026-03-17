---
type: concept
language: zh-CN
source_concept_note: "[[Parameter Sharing in NAS]]"
aliases: [NAS参数共享, 权重共享NAS]
---

# Parameter Sharing in NAS 中文条目

## 一句话直觉

参数共享 NAS 的思路是“先训一个超网，候选架构共用这套权重”，从而大幅降成本；但代价是候选排序可能失真。

## 它为什么重要

没有参数共享，很多 NAS 方法在算力上几乎不可用。参数共享是 one-shot 与可微 NAS 能落地的核心工程技巧之一。

## 一个小例子

两个候选 cell 都含有 `3x3 conv` 边时，超网会复用同一组卷积参数。这样无需为每个候选单独训练，但共享权重可能偏向某些结构，导致排名不可靠。

## 更正式的定义

在 NAS 中，参数共享是指：多个候选架构共同优化并复用一组网络权重，通过共享权重下的验证表现近似评估候选优劣，而非逐个从头训练。

## 数学形式（如有必要）

设候选架构 `a ∈ A`，共享权重 `W`，训练损失 `L_train(a, W)`，评价信号 `R(a, W)`。

超网阶段近似优化：

`min_W E_{a~p(a)} [ L_train(a, W) ]`

搜索阶段用 `R(a, W)` 排序候选，而不是对每个 `a` 单独训练后再比较。

## 核心要点

1. 它是 one-shot / 可微 NAS 的主要加速来源。
2. 排序偏差是常见问题，因为共享权重不可能对所有候选都最优。
3. BN 统计和采样策略会显著影响排序相关性。

## 这篇论文里怎么用

- [[NAS-Bench-201]]: 在统一 benchmark 上系统比较了参数共享与非参数共享方法，并展示 BN 处理对 one-shot 评估质量的影响（Sec. 5, Table 5, Table 7, Fig. 7-8）。

## 代表工作

- One-shot NAS 家族（如 ENAS）: 参数共享范式的早期代表。
- 可微 NAS 家族（如 DARTS）: 共享权重下的连续松弛优化代表。
- [[NAS-Bench-201]]: 通过统一评测揭示参数共享方法的典型失效模式。

## 相关概念

- [[One-shot NAS]]
- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]
