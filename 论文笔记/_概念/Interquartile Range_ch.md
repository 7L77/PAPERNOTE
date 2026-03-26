---
type: concept
language: zh-CN
source_concept_note: "[[Interquartile Range]]"
aliases: [四分位距, Interquartile Range]
---

# Interquartile Range 中文条目

## 一句话直觉

IQR（四分位距）只看数据中间 50% 的跨度，所以比均值/方差更不怕离群值。

## 它为什么重要

在噪声重尾场景里，离群点很常见。IQR 能帮助我们更稳健地识别异常贡献和异常样本。

## 一个小例子

数据有一个特别大异常值时，均值会被拉偏；IQR 主要由中间样本决定，受影响较小。

## 更正式的定义

设 \(Q_1\) 是第 25 百分位，\(Q_3\) 是第 75 百分位，则
\[
\mathrm{IQR}=Q_3-Q_1
\]

常见离群判据：
\[
x<Q_1-1.5\mathrm{IQR}\quad \text{或}\quad x>Q_3+1.5\mathrm{IQR}
\]

## 数学形式（如有必要）

IQR 属于分位数统计方法，适合非高斯、重尾分布。

## 核心要点

1. 抗离群值能力强。
2. 常用于异常检测。
3. 与 MoM 等稳健估计常一起使用。

## 这篇论文里怎么用

- [[RDNAS]]: 在 ROSE 里用 IQR 检测边际增益异常点，避免稀有但关键的操作被忽略。

## 代表工作

- [[RDNAS]]: IQR + MoM 组合用于鲁棒 NAS 操作打分。

## 相关概念

- [[Median-of-Means]]
- [[Shapley Value]]
