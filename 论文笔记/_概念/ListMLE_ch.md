---
type: concept
language: zh-CN
source_concept_note: "[[ListMLE]]"
aliases: [ListMLE, Listwise MLE]
---

# ListMLE 中文条目

## 一句话直觉

ListMLE 不是只看样本对，而是直接让模型去拟合“整张排序列表”的正确顺序。

## 它为什么重要

在 NAS predictor 中，我们通常关心候选列表整体排序质量，ListMLE 往往比纯回归更贴近这个目标。

## 一个小例子

若真实顺序是 A > B > C，ListMLE 会要求模型整体上给这个顺序更高概率，而不是只单独满足 A>B、B>C。

## 更正式的定义

设 \(\pi\) 为按真实性能从高到低的排列：
\[
\mathcal{L}_{ListMLE}=-\sum_{i=1}^{n}\log\frac{\exp(\hat{y}_{\pi(i)})}{\sum_{k=i}^{n}\exp(\hat{y}_{\pi(k)})}
\]

## 数学形式（如有必要）

- \(\pi(i)\): 真实排序第 \(i\) 位的样本索引。
- \(\hat{y}_{\pi(i)}\): 该样本预测分数。
- 损失越小，预测排序与真实排序越一致。

## 核心要点

1. 属于 listwise 排序目标。
2. 优化对象是整张列表的一致性。
3. 在低样本到中样本阶段常作为稳定 warm-up 选择。

## 这篇论文里怎么用

- [[PWLNAS]]: 把 ListMLE 作为 listwise 代表方法，并在 NAS-Bench-101 的分段策略中用于前期训练。

## 代表工作

- [[PWLNAS]]: 系统比较 ListMLE 与其他损失家族在 NAS predictor 中的表现。

## 相关概念

- [[Listwise Ranking Loss]]
- [[Pairwise Ranking Loss]]
