---
type: concept
language: zh-CN
source_concept_note: "[[WARP Loss]]"
aliases: [WARP, Weighted Approximate-Rank Pairwise]
---

# WARP Loss 中文条目

## 一句话直觉

WARP 是“带排序权重的 pairwise loss”：不仅惩罚排序错误，还会对头部样本的错误给更重惩罚。

## 它为什么重要

NAS 的核心是尽快命中高性能架构，WARP 这种 top-aware 目标通常更符合真实搜索需求。

## 一个小例子

若 A 本应排在很前面，却被预测到 B 后面，WARP 的惩罚会比普通 pairwise loss 更大。

## 更正式的定义

常见形式：
\[
\mathcal{L}_{WARP}=\sum_i\sum_{j\in\mathcal{N}_i}L(rank_i)\cdot\max(0,1-\hat{y}_i+\hat{y}_j)
\]

## 数学形式（如有必要）

- \(\mathcal{N}_i\): 与样本 \(i\) 比较的负样本集合。
- \(L(rank_i)\): 与真实排序位置相关的权重。
- 越靠前的样本，排序错误代价越大。

## 核心要点

1. 本质是 pairwise，但附加 rank 权重。
2. 对 top-ranking 指标通常更友好。
3. 对采样与 backbone 能力有一定敏感性。

## 这篇论文里怎么用

- [[PWLNAS]]: 将 WARP 引入 predictor-based NAS，并在 NAS-Bench-101、TransNAS 任务里作为后期或组合损失。

## 代表工作

- [[PWLNAS]]: 报告了 WARP 在头部识别上的竞争力。

## 相关概念

- [[Pairwise Ranking Loss]]
- [[Piecewise Loss Function]]
