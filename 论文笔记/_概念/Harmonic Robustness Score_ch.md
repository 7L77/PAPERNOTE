---
type: concept
language: zh-CN
source_concept_note: "[[Harmonic Robustness Score]]"
aliases: [调和鲁棒评分, HRS]
---

# Harmonic Robustness Score 中文条目

## 一句话直觉
HRS 是把 clean accuracy 与对抗鲁棒性合并的平衡指标，要求两者都好才会拿高分。

## 它为什么重要
只看单一指标会掩盖权衡关系；HRS 会惩罚“偏科”，更适合比较 robust NAS 方法。

## 一个小例子
某模型 clean 很高但鲁棒性很差，HRS 可能低于 clean 略低但鲁棒更强且更均衡的模型。

## 更正式的定义
HRS 是对自然精度与鲁棒性做调和式聚合的综合分数（REP 实验中采用）。

## 核心要点
1. 鼓励均衡表现，防止单指标过拟合。
2. 适合鲁棒 NAS 的综合评估。
3. 最好与各攻击下鲁棒指标一起看。

## 这篇论文里怎么用
- [[REP]] 在 CNN/GNN 多组对比中报告 HRS，并在文中汇报为最优。

## 代表工作
- [[REP]]: 使用 HRS 衡量“自然精度-鲁棒性”综合质量。

## 相关概念
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Neural Architecture Search]]

