---
type: concept
language: zh-CN
source_concept_note: "[[Differentiable Architecture Search]]"
aliases: [可微架构搜索, DARTS-style NAS]
---

# Differentiable Architecture Search 中文条目

## 一句话直觉

可微架构搜索把“选哪种网络结构”改写成连续可导的优化问题，这样我们就能直接用梯度来搜索架构。

## 它为什么重要

相比 RL 或进化式 NAS，它显著降低了搜索成本，让 NAS 在有限算力下也能落地。

## 一个小例子

一条边可以选 `3x3 conv` 或 `skip`。DARTS 不直接二选一，而是先给它们分配可学习权重，训练后再离散化选出最终操作。

## 更正式的定义

Differentiable Architecture Search 通过 softmax 或 Gumbel-softmax 这类连续松弛，把原本离散的结构决策参数化，并与网络权重一起做联合或双层优化。

## 数学形式（如有必要）

\[
\bar{o}(x) = \sum_{o \in \mathcal{O}} \text{softmax}(\alpha)_o \cdot o(x)
\]

其中 `alpha` 是架构参数，`\mathcal{O}` 是候选操作集合。

## 核心要点

1. 它把组合搜索问题转成了梯度优化问题。
2. 常见做法是双层优化：训练集更新网络权重，验证集更新架构参数。
3. 连续松弛后的搜索过程和最后离散化得到的网络之间，可能存在不一致，进而带来不稳定或 collapse。
4. 在经典 DARTS cell 里，每条 DAG 边都不是直接选一个 op，而是对多个 candidate op 做 softmax 加权混合。
5. 常见目标可写成 `min_alpha L_val(w*(alpha), alpha)`，其中 `w*(alpha) = argmin_w L_train(w, alpha)`；这意味着架构参数和 supernet 权重在搜索时是紧耦合的。

## 这篇论文里怎么用

- [[ROME]]: 在单路径可微 NAS 框架上，通过拓扑解耦和梯度累积缓解 collapse 与不稳定问题。
- [[LLMENAS]]: 在 `III.B` 里把 DARTS 当作标准的 gradient-based NAS 背景来回顾，先说明连续松弛、mixed op 和双层优化是怎么工作的。
- [[LLMENAS]]: 这一节的重点不是改 DARTS 公式，而是说明它为什么会偏向 `skip` 这类无参数操作、为什么容易陷入局部最优，从而为后面的 CMA-ES 与 LLM fitness design 做铺垫。

## 代表工作

- [[DARTS]]: 可微 NAS 的经典代表。
- [[GDAS]]: 基于 Gumbel 采样的单路径可微 NAS。
- [[LLMENAS]]: 把 DARTS 作为核心 gradient-based baseline，并借其局限性引出分层进化式替代方案。

## 相关概念

- [[Neural Architecture Search]]
- [[One-shot NAS]]
