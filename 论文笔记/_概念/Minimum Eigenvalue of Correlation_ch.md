---
type: concept
language: zh-CN
source_concept_note: "[[Minimum Eigenvalue of Correlation]]"
aliases: [相关矩阵最小特征值]
---

# Minimum Eigenvalue of Correlation 中文条目

## 一句话直觉
相关矩阵的最小特征值越大，通常表示表示空间越不容易在某些方向上退化或塌缩。

## 为什么重要
在训练前 NAS 的 proxy 设计里，它可以作为低成本频谱统计量，帮助排序候选架构。

## 小例子
两个候选网络在多层上得到的相关矩阵里，若网络 A 的 `lambda_min` 普遍高于网络 B，则 MeCo 往往更偏向 A。

## 定义
对相关矩阵 `P`，最小特征值定义为:

$$
\lambda_{min}(P)=\min_i \lambda_i(P)
$$

## 核心要点
1. 对相关矩阵是否接近奇异很敏感。
2. 小样本下数值稳定性需要特别注意。
3. 在 proxy 里通常按层聚合使用。

## 在本论文中的使用
- [[MeCo]] 使用:
  `S_MeCo = sum_l lambda_min(P(F_l(X)))`。
- 该分数用于 zero-shot NAS 候选排序。

## 代表工作
- [[MeCo]]

## 相关概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Spearman's Rank Correlation]]
