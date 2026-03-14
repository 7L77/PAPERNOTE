---
type: concept
language: zh-CN
source_concept_note: "[[Kendall's Tau]]"
aliases: [肯德尔秩相关, KT]
---

# Kendall's Tau 中文条目

## 一句话直觉
Kendall's Tau 用“样本对顺序是否一致”来衡量两个排序之间的相似度。

## 它为什么重要
NAS 里很多方法输出的是候选架构排序，Tau 可以直接评估这个排序是否接近真实性能排序。

## 一个小例子
如果两个排序里大多数架构对的先后关系一致，Tau 就高；若经常颠倒，Tau 就低甚至为负。

## 更正式的定义
Kendall's Tau 是基于一致对（concordant）与不一致对（discordant）数量构造的秩相关系数。

## 数学形式（如有必要）
\[
\tau = \frac{C - D}{\binom{n}{2}}
\]
其中 `C` 为一致对数，`D` 为不一致对数。

## 核心要点
1. `tau=1` 表示排序完全一致。
2. `tau=0` 表示几乎无序相关。
3. `tau<0` 表示整体排序趋势相反。

## 这篇论文里怎么用
- [[AZ-NAS]]: 在 NAS-Bench-201 上以 Kendall's Tau 作为主排序指标。

## 代表工作
- Kendall, 1938.

## 相关概念
- [[NAS-Bench-201]]
- [[Non-linear Ranking Aggregation]]

