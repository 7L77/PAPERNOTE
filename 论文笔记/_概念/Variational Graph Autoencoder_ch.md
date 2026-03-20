---
type: concept
language: zh-CN
source_concept_note: "[[Variational Graph Autoencoder]]"
aliases: [VGAE, 图变分自编码器]
---

# Variational Graph Autoencoder 中文条目

## 一句话直觉
Variational Graph Autoencoder, 简称 VGAE, 会把图结构压成连续潜变量，再从潜变量重建原图。

## 它为什么重要
它把离散图对象变成了可以做梯度优化的连续表示，这对架构搜索尤其关键。

## 一个小例子
把 cell 架构看成 DAG 后，VGAE 可以先把它编码成向量 `Z`，再在 `Z` 上做优化，最后解码回新的架构。

## 更正式的定义
VGAE 是图上的变分自编码器，用图编码器推断潜变量，用图解码器重建边和节点属性，并用 KL 正则让潜空间更平滑。

## 核心要点
1. 适合把离散图搜索问题改写成连续优化问题。
2. KL 项会让潜空间比普通 autoencoder 更规整。
3. 如果解码器重建差，后续搜索得到的潜变量就难以落回合法图结构。

## 这篇论文里怎么用
- [[UP-NAS]]: 借助 `arch2vec` 风格的 VGAE 把架构映射到连续潜空间，然后在潜空间中做梯度上升搜索。

## 代表工作
- Kipf 和 Welling在 2016 年提出了经典 VGAE 形式。

## 相关概念
- [[Architecture Embedding]]
- [[Graph Isomorphism Network]]
- [[Neural Architecture Search]]
