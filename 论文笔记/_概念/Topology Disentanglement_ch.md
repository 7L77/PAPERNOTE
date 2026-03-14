---
type: concept
language: zh-CN
source_concept_note: "[[Topology Disentanglement]]"
aliases: [拓扑解耦, Topology-Operation Decoupling]
---

# Topology Disentanglement 中文条目

## 一句话直觉

把“连哪条边”和“边上用哪个算子”分开优化，可以减少架构搜索里的结构不一致问题。

## 它为什么重要

很多可微 NAS 在搜索阶段和评估阶段的图结构不同，容易导致 collapse。拓扑解耦能把这种差异提前消掉。

## 一个小例子

DARTS 风格 cell 最终每个中间节点只保留 2 条入边。如果搜索期一直让所有候选边都参与，训练到的超网与最终离散网络并不一致。TD 会在搜索期就按 2 条边约束采样。

## 更正式的定义

Topology Disentanglement 使用独立变量表示“边是否存在”和“边上算子选择”，并在显式拓扑约束下联合优化。

## 数学形式（如有必要）

- `B_{i,j}`: 边 `(i,j)` 是否被选。
- `A^o_{i,j}`: 边 `(i,j)` 上算子 `o` 是否被选。
- 约束: 每个中间节点入度固定为 2。

## 核心要点

1. 拓扑选择与算子选择显式解耦。
2. 缓解搜索-评估不一致。
3. 常用于提升可微 NAS 的稳定性。

## 这篇论文里怎么用

- [[ROME]]: 用 `beta` 建模边重要性，并通过 in-degree 约束采样边，显著降低 skip collapse。

## 代表工作

- [[ROME]]: 在单路径可微 NAS 中系统采用 TD。
- [[DOTS]]: 讨论拓扑与算子解耦思路的相关工作。

## 相关概念

- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]

