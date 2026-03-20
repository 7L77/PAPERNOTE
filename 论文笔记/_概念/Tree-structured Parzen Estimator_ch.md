---
type: concept
language: zh-CN
source_concept_note: "[[Tree-structured Parzen Estimator]]"
aliases: [TPE, 树结构 Parzen 估计]
---

# Tree-structured Parzen Estimator 中文条目

## 一句话直觉
Tree-structured Parzen Estimator, 简称 TPE, 是一种黑盒超参数搜索方法，会根据历史结果把更多采样预算放到更有希望的参数区域。

## 它为什么重要
当目标函数不可导、很贵、或者只能试出来时，TPE 往往比人工调参和穷举更实际。

## 一个小例子
如果我们要给 13 个 zero-cost proxy 找组合权重，TPE 会优先继续探索那些曾经带来更高排序相关性的权重区域。

## 更正式的定义
TPE 属于序贯模型优化方法，不直接拟合“参数到目标”的回归，而是通过建模不同目标值条件下的参数分布来指导下一轮采样。

## 核心要点
1. 适合混合型、不可导、非凸的超参数空间。
2. 常见实现是 Optuna。
3. 效果取决于评估预算和目标指标本身的稳定性。

## 这篇论文里怎么用
- [[UP-NAS]]: 用 TPE 搜索统一代理里的权重 `lambda`，目标是让统一代理与真实精度的 [[Kendall's Tau]] 最大。

## 代表工作
- Bergstra 等人在 2011 年提出 TPE 框架，是这类方法的经典来源。

## 相关概念
- [[Kendall's Tau]]
- [[Unified Proxy]]
- [[Zero-Cost Proxy]]

