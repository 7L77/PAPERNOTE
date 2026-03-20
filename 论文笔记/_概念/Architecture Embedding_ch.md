---
type: concept
language: zh-CN
source_concept_note: "[[Architecture Embedding]]"
aliases: [架构嵌入, 架构潜表示]
---

# Architecture Embedding 中文条目

## 一句话直觉
Architecture Embedding 就是把离散神经网络架构压成一个连续向量表示。

## 它为什么重要
有了连续表示，我们就能用预测器、聚类、最近邻、甚至梯度优化去操作架构，而不只是靠离散枚举。

## 一个小例子
把一个 NAS cell 编成向量 `Z` 后，我们可以在 `Z` 上训练代理模型，或者沿梯度方向移动 `Z` 再解码成新架构。

## 更正式的定义
Architecture Embedding 是编码器给离散架构生成的潜表示，希望在连续空间里保留对搜索有用的结构信息和相似性。

## 核心要点
1. 好的 embedding 要同时保留拓扑和操作信息。
2. 如果想在潜空间中优化，embedding 的平滑性很关键。
3. 它常被用于预测器驱动 NAS、检索和结构分析。

## 这篇论文里怎么用
- [[UP-NAS]]: 先把架构编码成潜向量，再由 MPE 预测 proxy，并直接在该向量上做梯度上升。

## 代表工作
- [[NAO]]: 用连续架构表示做 predictor-guided search。
- `arch2vec`: 用无监督方式学习架构表示。

## 相关概念
- [[Variational Graph Autoencoder]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]

