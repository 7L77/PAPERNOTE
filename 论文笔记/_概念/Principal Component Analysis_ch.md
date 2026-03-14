---
type: concept
language: zh-CN
source_concept_note: "[[Principal Component Analysis]]"
aliases: [主成分分析, PCA]
---

# Principal Component Analysis 中文条目

## 一句话直觉

PCA（主成分分析）是在“尽量少维度”下保留“尽量多变化信息”的线性变换方法。

## 它为什么重要

很多高维表示有冗余，PCA 可以把关键信息压到前几个方向，便于分析与建模。

## 一个小例子

二维点云如果大多沿一条斜线分布，那么第一个主成分就接近那条斜线，1 维近似就很有效。

## 更正式的定义

对中心化后的数据，计算协方差矩阵并做特征分解。特征值越大，对应主成分解释的方差越多。

## 数学形式（如有必要）

若特征值为 `lambda_1 >= lambda_2 >= ...`，第 `k` 个主成分解释比例为
`lambda_k / sum_i lambda_i`。

## 核心要点

1. PCA 不需要标签，是无监督方法。
2. 特征值谱反映信息分布是否集中。
3. 选多少主成分本质是压缩与保真权衡。

## 这篇论文里怎么用

- [[W-PCA]]: 在 FFN 隐状态上用 PCA 维度作为零训练代理的一部分。

## 代表工作

- [[W-PCA]]: 把 PCA 维度与参数量相乘构造 W-PCA 代理。

## 相关概念

- [[Cumulative Explained Variance]]
- [[Training-free NAS]]
