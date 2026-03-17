---
type: concept
language: zh-CN
source_concept_note: "[[Graph Attention Network]]"
aliases: [图注意力网络, Graph Attention Network]
---

# Graph Attention Network 中文条目

## 一句话直觉
Graph Attention Network（GAT）是在图上做“有偏好”的邻居聚合：不同邻居贡献不同。

## 它为什么重要
NAS 的候选架构天然是图结构，GAT 能更好提取哪些连接和操作对架构表示更关键。

## 一个小例子
在 cell 图里，某个节点可能更依赖来自卷积操作节点的信息，GAT 会给这类邻居更高权重。

## 更正式的定义
GAT 在图边上学习注意力系数，再对邻居特征进行加权聚合，得到新的节点表示，可堆叠多层得到图级表示。

## 核心要点
1. 邻居权重由模型学习，不是固定平均。
2. 多头注意力提升表示能力与稳定性。
3. 适合结构关系对任务结果影响明显的图数据。

## 这篇论文里怎么用
- [[PO-NAS]]: 在预训练阶段用两层 GAT 编码架构图，输出用于后续代理模型的架构 embedding。

## 代表工作
- [[Graph Attention Networks]]: GAT 原始论文。
- [[PO-NAS]]: 在 NAS 代理评分中使用 GAT 架构编码。

## 相关概念
- [[Cross-Attention]]
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
