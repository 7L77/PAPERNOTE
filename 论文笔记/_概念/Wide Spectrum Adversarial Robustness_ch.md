---
type: concept
language: zh-CN
source_concept_note: "[[Wide Spectrum Adversarial Robustness]]"
aliases: [宽谱对抗鲁棒性, Wide Spectrum Adversarial Robustness]
---

# Wide Spectrum Adversarial Robustness 中文条目

## 一句话直觉

鲁棒性不该只看一个攻击强度点，而要看模型在“一段强度范围”内是否都稳。

## 它为什么重要

真实攻击强度并不固定。只在单点 \(\epsilon\) 上优化的模型，往往在更强或偏移强度下掉得很快。

## 一个小例子

模型 A 在 \(\epsilon=0.03\) 最好，但在 \(\epsilon=0.17\) 明显崩；模型 B 在 0.03 略差，却在 0.06-0.25 区间更稳。宽谱鲁棒性会倾向模型 B。

## 更正式的定义

可用多强度平均鲁棒准确率衡量：
\[
\text{AvgRobustAcc}=\frac{1}{K}\sum_{k=1}^K \text{Acc}(\epsilon_k).
\]

## 数学形式（如有必要）

给定强度集合 \(\{\epsilon_1,...,\epsilon_K\}\)，分别评估后做均值或加权均值，作为比较与优化依据。

## 核心要点

1. 它是“跨强度分布”的视角，不是单点评分。
2. 重点是鲁棒性的稳定性，而非某一个 \(\epsilon\) 峰值。
3. 计算成本更高，通常需要额外降本设计。

## 这篇论文里怎么用

- [[Wsr-NAS]]: 直接把多强度损失纳入 NAS 目标，并在多 \(\epsilon\) 下报告平均鲁棒准确率。

## 代表工作

- [[Wsr-NAS]]: 用 NAS 明确优化宽谱对抗鲁棒性。

## 相关概念

- [[Adversarial Robustness]]
- [[Robust Search Objective]]
- [[PGD Attack]]
- [[Adversarial Noise Estimator]]

