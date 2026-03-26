---
type: concept
language: zh-CN
source_concept_note: "[[Median-of-Means]]"
aliases: [分组均值中位数, Median-of-Means]
---

# Median-of-Means 中文条目

## 一句话直觉

Median-of-Means（MoM）就是“先分组求均值，再对均值取中位数”，用中位数来压制离群值对整体估计的破坏。

## 它为什么重要

在对抗训练或 NAS 搜索中，统计量常有重尾噪声。MoM 可以减少“少数极端样本”导致的估计漂移，提升排序稳定性。

## 一个小例子

一组样本中混入几个特别大的异常值时，直接平均会明显偏高；MoM 先分组后取组均值中位数，异常值只污染少数组，最终结果更稳。

## 更正式的定义

将样本划分为 \(G\) 组，组均值为 \(\mu_g\)，则
\[
\mathrm{MoM}=\mathrm{median}(\mu_1,\dots,\mu_G)
\]

## 数学形式（如有必要）

\[
\mu_g=\frac{1}{|B_g|}\sum_{i\in B_g}x_i,\quad
\mathrm{MoM}=\mathrm{median}(\mu_1,\dots,\mu_G)
\]

其中 \(B_g\) 是第 \(g\) 个样本子集。

## 核心要点

1. 对离群值更不敏感。
2. 适合重尾噪声环境。
3. 分组数是关键超参数。

## 这篇论文里怎么用

- [[RDNAS]]: 在 ROSE 中，MoM 用来稳定 operation 的边际增益估计，降低 run-to-run 方差。

## 代表工作

- [[RDNAS]]: MoM + IQR 的组合用于鲁棒 Shapley 打分。

## 相关概念

- [[Interquartile Range]]
- [[Shapley Value]]
