---
type: concept
language: zh-CN
source_concept_note: "[[Isomorphic Architectures]]"
aliases: [同构架构, 架构同构]
---

# Isomorphic Architectures 中文条目

## 一句话直觉
两个看起来不同的架构编码，可能对应同一个计算图，本质上是同一个网络结构。

## 它为什么重要
如果不去重，会把“同一个模型”重复统计，导致 benchmark 评估和搜索结论偏差。

## 一个小例子
某条 skip 连接可能让另一条边操作失效，于是两种编码虽然字符串不同，但计算过程等价。

## 更正式的定义
在 NAS 图空间中，若两个架构存在保持连接关系与操作语义的映射，并产生等价计算图，则称它们同构。

## 数学形式（如有必要）
设计算图为 `G1, G2`。若存在双射 `phi`，使邻接关系与操作标签在 `phi` 下保持（考虑语义等价），则 `G1` 与 `G2` 同构。

## 核心要点
1. Tabular benchmark 必须先做同构规约。
2. 同构去重能显著缩小有效搜索空间。
3. 下游分析要使用 canonical id（如 `uid`）避免重复计数。

## 这篇论文里怎么用
- [[NADR-Dataset]]: 从 15,625 个编码架构规约到 6,466 个非同构架构，并以此作为评测全集。

## 代表工作
- Dong and Yang, NAS-Bench-201 (2020).
- Jung et al., ICLR 2023.

## 相关概念
- [[NAS-Bench-201]]
- [[Neural Architecture Search]]
- [[NADR-Dataset]]

