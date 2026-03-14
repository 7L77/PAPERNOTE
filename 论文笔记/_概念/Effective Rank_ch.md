---
type: concept
language: zh-CN
source_concept_note: "[[Effective Rank]]"
aliases: [有效秩, 有效维度]
---

# Effective Rank 中文条目

## 一句话直觉
有效秩衡量的是矩阵“真正有效使用了多少维度”，而不是仅看代数意义上的非零秩。

## 为什么重要
同样是满秩矩阵，可能存在两种情况:
1. 能量几乎都集中在一个方向，表示容易塌缩。
2. 能量在多个方向更均衡，表示能力更丰富。

有效秩可以区分这两种情况。

## 小例子
如果奇异值分布是“一个很大、其余很小”，普通秩可能仍是满秩，但有效秩会偏低。  
如果奇异值更均匀，有效秩会更高。

## 定义
给定矩阵 `A` 的奇异值 `\sigma_k`:
\[
p_k = \frac{\sigma_k}{\sum_i \sigma_i}, \quad
H(p) = -\sum_k p_k \log p_k, \quad
\mathrm{erank}(A)=\exp(H(p)).
\]

## 核心要点
1. 本质是“归一化奇异值熵”的指数形式。
2. 能反映谱分布是否失衡，而不只看是否为零。
3. 适合评估表示是否塌缩、维度利用是否充分。

## 在这篇论文里怎么用
- [[NEAR]]: 逐层计算预激活与后激活矩阵的有效秩并求和，作为 zero-cost 代理分数。

## 代表工作
- Roy and Vetterli, "The effective rank: A measure of effective dimensionality" (2007).
- Husistein et al., "NEAR" (ICLR 2025).

## 相关概念
- [[Network Expressivity]]
- [[Zero-Cost Proxy]]
- [[Spectral Norm]]

