---
type: concept
language: zh-CN
source_concept_note: "[[Kronecker Product]]"
aliases: [克罗内克积, 张量积]
---

# Kronecker Product 中文条目

## 一句话直觉
Kronecker 积把两个矩阵“展开融合”为一个更大的分块矩阵，用于表达两种结构的组合关系。

## 它为什么重要
当我们要同时建模两类相似性/协方差时，Kronecker 积是一种结构清晰的融合方式。

## 一个小例子
`2x2` 矩阵和 `2x2` 矩阵做 Kronecker 积会得到 `4x4` 矩阵，每个块都是“前者元素乘以后者整块”。

## 更正式的定义
若 `A in R^{m x n}`，`B in R^{p x q}`，则
\[
A \otimes B \in R^{mp \times nq}
\]
并且块结构由 `a_ij * B` 构成。

## 核心要点
1. 维度按乘法扩展。
2. 在方阵情形下有行列式恒等关系，可用于推导简化。
3. 常用于多视角结构融合。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 用 `log|K ⊗ Q|` 聚合两路相似矩阵信息。
- 随后化简为 `N(log|K| + log|Q|)` 提升计算效率。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[Radial Basis Function Kernel]]
- [[Neural Architecture Search]]

