---
type: concept
language: zh-CN
source_concept_note: "[[NAS-Bench-101]]"
aliases: [NAS-Bench-101, NB101]
---

# NAS-Bench-101 中文条目

## 一句话直觉
NAS-Bench-101 是把大量候选架构“先训练好再存成表”的 NAS 基准，你可以直接查精度做方法对比。

## 它为什么重要
它显著降低了 NAS 对比实验成本，并提升了可复现性与公平性。

## 一个小例子
做排序器时，不需要每个候选都重训，只需预测分数并和 NB101 的真值精度排名做相关性对比。

## 更正式的定义
NAS-Bench-101 是一个基于固定 CNN cell 搜索空间的表格化基准，提供统一协议下的多次训练结果。

## 数学形式（如有必要）
通常用预测排序与真值排序的相关系数（如 KD/SP）来评估方法质量。

## 核心要点
1. 适合快速、可复现的 NAS 排序研究。
2. 特别适合低样本 predictor 对比。
3. 外推到更大/异构搜索空间时需谨慎。

## 这篇论文里怎么用
- [[ParZC]]: 在 NB101 上报告了显著的排序相关性与样本效率提升。

## 代表工作
- [[ParZC]]: 用 NB101 做 predictor 与 zero-cost 方法对比。

## 相关概念
- [[NAS-Bench-201]]
- [[Neural Architecture Search]]
- [[Kendall's Tau]]
