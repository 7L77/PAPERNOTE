---
type: concept
language: zh-CN
source_concept_note: "[[Non-linear Ranking Aggregation]]"
aliases: [非线性排名聚合, Rank聚合]
---

# Non-linear Ranking Aggregation 中文条目

## 一句话直觉
非线性排名聚合不会简单平均各指标，而是对短板项施加更大惩罚，要求候选在多维指标上都比较均衡。

## 它为什么重要
多 proxy 场景下，线性加和容易“以长补短”掩盖问题；非线性聚合可降低这种风险。

## 一个小例子
某候选在 3 个 proxy 排名靠前、1 个排名很差，线性和可能仍高；log-rank 聚合会把它明显拉低。

## 更正式的定义
将各指标的排名通过非线性变换（如对数）后再融合的排序策略，用于强化全维度稳健性。

## 数学形式（如有必要）
AZ-NAS 使用：
\[
s(i)=\sum_m \log(\mathrm{Rank}_m(i)/N)
\]

## 核心要点
1. 强调“全面好”而非“单项极强”。
2. 能抑制线性补偿效应。
3. 对排序式选择更稳健。

## 这篇论文里怎么用
- [[AZ-NAS]]: 对 `sE/sP/sT/sC` 的 rank 做 log 求和，得到最终 AZ 分。

## 代表工作
- Lee and Ham, AZ-NAS (CVPR 2024).

## 相关概念
- [[Zero-Cost Proxy]]
- [[Kendall's Tau]]

