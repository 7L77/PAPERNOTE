---
type: concept
language: zh-CN
source_concept_note: "[[Cramer-Rao Bound]]"
aliases: [Cramer-Rao下界, CRB]
---

# Cramer-Rao Bound 中文条目

## 一句话直觉

Cramer-Rao 下界说明：在无偏估计条件下，参数方差不可能无限小，存在由信息量决定的理论下限。

## 它为什么重要

它把“数据与模型有多少可用信息”与“参数估计能有多稳定”直接联系起来，是分析训练难度的理论工具。

## 一个小例子

两个模型在同样数据量下，如果一个模型对应更大的 Fisher 信息，那么它的最小可达估计方差更低，通常更容易稳定学习。

## 更正式的定义

设无偏估计量为 `theta_hat`，样本数为 `n`，FIM 为 `F(theta)`，则有：

`Var(theta_hat) >= (1/n) * F(theta)^(-1)`。

## 数学形式（如有必要）

VKDNW 在 Sec. II-A 的 Eq. (3) 使用该下界来解释 FIM 谱与可估计性的关系。

## 核心要点

1. 这是理论下界，不保证有限样本一定达到。
2. 信息量越大（FIM 越“强”），方差下界越低。
3. 可用于解释为何 FIM 谱能作为训练可行性的 proxy。

## 这篇论文里怎么用

- [[VKDNW]]: 借助 CRB 解释“谱越均衡越可训练”的动机。

## 代表工作

- [[VKDNW]]: 在 training-free NAS 中引入 CRB 视角。

## 相关概念

- [[Fisher Information Matrix]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
