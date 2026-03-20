---
type: concept
language: zh-CN
source_concept_note: "[[Graph Isomorphism Network]]"
aliases: [GIN, 图同构网络]
---

# Graph Isomorphism Network 中文条目

## 一句话直觉
Graph Isomorphism Network, 简称 GIN, 是一种特别强调“分清图结构差异”的图神经网络。

## 它为什么重要
在 NAS 里，两个架构可能操作差不多，但连边方式不同；如果编码器分不清这些结构差异，后面的潜空间搜索就会变钝。

## 一个小例子
两个 cell 都有卷积和跳连，但边连接顺序不同。GIN 比较擅长把这种结构差异保留到 embedding 里。

## 更正式的定义
GIN 是一种消息传递 GNN，它的聚合更新形式和 Weisfeiler-Lehman 图同构测试有关，因此在常见 GNN 里表达能力较强。

## 核心要点
1. 适合结构辨别能力要求高的图任务。
2. 常用邻居特征求和后接 MLP 的形式。
3. 在 NAS 里，它能同时编码拓扑和操作差异。

## 这篇论文里怎么用
- [[UP-NAS]]: 用 GIN 来实现架构编码器，生成图潜变量的均值和方差。

## 代表工作
- Xu 等人在 2019 年提出 GIN，并从表达能力角度解释它为什么强。

## 相关概念
- [[Variational Graph Autoencoder]]
- [[Architecture Embedding]]
- [[Neural Architecture Search]]

