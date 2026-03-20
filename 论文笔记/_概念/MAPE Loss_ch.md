---
type: concept
language: zh-CN
source_concept_note: "[[MAPE Loss]]"
aliases: [MAPE, Mean Absolute Percentage Error Loss]
---

# MAPE Loss 中文条目

## 一句话直觉

MAPE Loss 关注相对误差而非绝对误差，在 NAS 场景中有助于放大高性能候选之间的细微差异。

## 它为什么重要

当多个强架构绝对精度非常接近时，相对误差式目标更容易把它们拉开，提升头部筛选质量。

## 一个小例子

两个样本绝对误差同为 0.01，但相对误差不同；MAPE 会给相对误差更大的那个更强惩罚。

## 更正式的定义

PWLNAS 代码中的形式（在 error 空间）：
\[
\mathcal{L}_{MAPE}=\frac{1}{n}\sum_i\left|\frac{(1-\hat{y}_i)-b}{(1-y_i)-b}-1\right|
\]

## 数学形式（如有必要）

- \(y_i\): 真实性能。
- \(\hat{y}_i\): 预测性能。
- \(b\): 下界稳定项，防止分母过小。
- 这里通过 \(1-y\) 把准确率映射到误差空间。

## 核心要点

1. 强调相对误差而非平方误差。
2. 常在样本量足够后更有效。
3. 与 predictor 骨干和搜索空间强相关。

## 这篇论文里怎么用

- [[PWLNAS]]: 把 MAPE 作为关键 weighted loss，并在 HR -> MAPE 的分段配置中获得强结果。

## 代表工作

- [[PWLNAS]]: 系统分析 MAPE 在 predictor-based NAS 的适用条件。

## 相关概念

- [[Piecewise Loss Function]]
- [[WARP Loss]]
