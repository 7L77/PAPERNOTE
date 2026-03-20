---
type: concept
language: zh-CN
source_concept_note: "[[Hierarchical Agglomerative Clustering]]"
aliases: [层次凝聚聚类, HAC]
---

# Hierarchical Agglomerative Clustering 中文条目

## 一句话直觉
层次凝聚聚类从“每个样本单独成簇”开始，不断合并最相近簇，最终得到一棵层级树。

## 为什么重要
当下游方法需要树结构决策（而不是一次性平坦划分）时，HAC 非常实用。

## 小例子
在 NAS 中用架构输出向量距离做 HAC，可以先聚成“功能相近”的小簇，再逐步合并成整棵搜索树。

## 定义
给定两两距离矩阵，按 linkage 准则（如 Ward）迭代合并簇，直到所有样本并为一个簇。

## 核心要点
1. 输出完整层级关系（dendrogram）。
2. 距离度量与 linkage 选择会显著影响结果。
3. 常见实现复杂度约为二次规模。

## 在本文中的作用
- [[MCTS-Learned Hierarchy]] 用架构输出距离矩阵做 agglomerative clustering 构造 MCTS 树（Sec.4, Algorithm 1）。

## 代表工作
- Murtagh and Legendre (2014)

## 相关概念
- [[Monte-Carlo Tree Search]]
- [[KL Divergence]]
- [[Neural Architecture Search]]
