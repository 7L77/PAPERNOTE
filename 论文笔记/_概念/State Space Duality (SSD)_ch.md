---
type: concept
language: zh-CN
source_concept_note: "[[State Space Duality (SSD)]]"
aliases: [状态空间对偶, SSD]
---

# State Space Duality (SSD) 中文条目

## 一句话直觉
SSD 可以理解为把选择性状态空间计算改写成一种“接近注意力张量运算”的形式，从而能借用注意力体系里的分析思路。

## 它为什么重要
在 Mamba2 里，SSD 是核心计算单元。很多关于表达能力、秩变化、代理设计的讨论都要从这里出发。

## 一个小例子
注意力常用 `Q/K/V` 交互来分析；在 TF-MAS 记号里，SSD 相关的 `C/B/X` 也形成类似可分析结构，因此可迁移部分直觉。

## 更正式的定义
SSD 是 Mamba2 使用的选择性状态空间计算表示方式，它把序列变换写成结构化矩阵/张量组合，并与线性注意力模式存在对偶关系。

## 数学形式（如有必要）
TF-MAS 文中把 SSD 输出写为类似
\[
Y = (L \circ (CB^\top))X
\]
其中 `L` 为结构项，`\circ` 表示论文中的逐元素交互。

## 核心要点
1. SSD 是 Mamba2 block 的核心。
2. 它是 Mamba2 与注意力分析对齐的桥梁。
3. TF-MAS 正是利用这个桥梁构建代理。

## 这篇论文里怎么用
- [[TF-MAS]]: 假设 SSD 堆叠存在 rank collapse 趋势，并据此定义训练免费架构评分。

## 代表工作
- [[TF-MAS]]: 基于 SSD 内部映射构造 Mamba2 代理。

## 相关概念
- [[Rank Collapse]]
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]

