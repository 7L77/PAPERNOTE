---
type: concept
language: zh-CN
source_concept_note: "[[N@K]]"
aliases: [Top-K Best Rank, Best Rank in Top-K]
---

# N@K 中文条目

## 一句话直觉

N@K 衡量的是：在 predictor 选出的 top-K 候选里，最好那个样本在真实全局排名里是第几名（越小越好）。

## 它为什么重要

预算受限时我们只会评估少量候选，N@K 直接反映“这批候选里有没有真正接近最优的架构”。

## 一个小例子

若 top-10 预测候选中最好的真实排名是第 2 名，则 N@10 = 2。

## 更正式的定义

令 \(X_K\) 为预测分数前 K 的集合，\(r_i\) 为真实排名：
\[
N@K=\min_{x_i\in X_K} r_i
\]

## 数学形式（如有必要）

- \(X_K\): 预测 top-K 样本集合。
- \(r_i\): 样本在全空间的真实排名。
- N@K 越小，说明在预算内命中高质量架构的能力越强。

## 核心要点

1. 是典型的头部导向指标。
2. 与最终搜索可得最优解高度相关。
3. 常与 [[Precision@T]]、[[Kendall's Tau]] 结合解读。

## 这篇论文里怎么用

- [[PWLNAS]]: 把 N@K 作为关键评测指标，分析不同损失在 top 架构发现能力上的差异。

## 代表工作

- [[PWLNAS]]: 在多搜索空间中系统报告 N@10 结果。

## 相关概念

- [[Precision@T]]
- [[Kendall's Tau]]
