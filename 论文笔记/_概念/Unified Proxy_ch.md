---
type: concept
language: zh-CN
source_concept_note: "[[Unified Proxy]]"
aliases: [统一代理, UP]
---

# Unified Proxy 中文条目

## 一句话直觉
Unified Proxy 就是把多个 zero-cost proxy 融成一个统一分数，让搜索只优化一个标量目标。

## 它为什么重要
单个 proxy 往往只擅长某一类场景，多 proxy 融合能减少偏置，也更容易形成稳定的搜索行为。

## 一个小例子
比如给 `jacov` 和 `synflow` 正权重、给 `params` 负权重，就能得到一个同时考虑表达性、可训练性和复杂度的统一分数。

## 更正式的定义
Unified Proxy 是由多个代理指标构成的聚合标量评分函数，目标是比单个代理更贴近真实性能排序。

## 核心要点
1. 最简单的形式是加权和。
2. 效果高度依赖权重怎么学、学完能不能迁移。
3. 好处是搜索端只需要优化一个数，但信息来自多个代理。

## 这篇论文里怎么用
- [[UP-NAS]]: 定义 `UP(A)=sum_i lambda_i f^i_zc(A)`，并把它作为潜空间梯度上升的直接目标。

## 代表工作
- [[UP-NAS]]: 较早明确提出 unified proxy 的训练自由 NAS 方案。
- [[PO-NAS]]: 后续工作进一步研究了更细粒度的多 proxy 融合。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Tree-structured Parzen Estimator]]
