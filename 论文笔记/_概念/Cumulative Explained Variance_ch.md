---
type: concept
language: zh-CN
source_concept_note: "[[Cumulative Explained Variance]]"
aliases: [累计解释方差, Explained Variance Threshold]
---

# Cumulative Explained Variance 中文条目

## 一句话直觉

累计解释方差表示“保留前 k 个主成分后，覆盖了总信息的多少比例”。

## 它为什么重要

它把“该保留多少维”变成可量化规则，是 PCA 实践中的关键阈值工具。

## 一个小例子

如果前 30 个主成分已覆盖 99% 方差，那就可以用 30 维近似原始高维表示。

## 更正式的定义

对降序特征值 `lambda_1 ... lambda_D`，累计解释方差为
`sum_{i=1..k} lambda_i / sum_{i=1..D} lambda_i`。

## 数学形式（如有必要）

给定阈值 `eta`，选择最小 `k` 满足累计解释方差 `>= eta`。

## 核心要点

1. 它把谱信息变成可比较的维度选择标准。
2. `eta` 越高，保真越高但维度也越大。
3. 同一 `eta` 下的 `k` 可用于模型间比较。

## 这篇论文里怎么用

- [[W-PCA]]: 用 `eta=0.99` 定义每层需要的主成分数 PCA_dim，并汇总成代理分数。

## 代表工作

- [[W-PCA]]: 将累计解释方差阈值作为零训练评分核心步骤。

## 相关概念

- [[Principal Component Analysis]]
- [[Zero-Cost Proxy]]
