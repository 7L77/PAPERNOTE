---
type: concept
language: zh-CN
source_concept_note: "[[Spearman's Rank Correlation]]"
aliases: [Spearman 秩相关, Spearman rho]
---

# Spearman's Rank Correlation 中文条目

## 一句话直觉
它看的是“排序是否一致”，不是“分数差多少”。

## 它为什么重要
NAS 里 proxy 的核心任务是把好架构排在前面，所以秩相关比绝对回归误差更关键。

## 一个小例子
真实性能排序是 A>B>C，proxy 排序也是 A>B>C，即便分数尺度不同，Spearman 仍会很高。

## 更正式的定义
把两个变量都转换成秩次后，再做皮尔逊相关；取值范围 \([-1,1]\)，1 表示完全同序。

## 核心要点
1. 衡量单调排序一致性。
2. 对保持顺序的非线性变换不敏感。
3. 是 zero-cost proxy 对比中的常用指标。

## 这篇论文里怎么用
- [[SWAP-NAS]]: 用 Spearman 对比 SWAP 及其正则版本与多种 baseline 的排序一致性。

## 代表工作
- [[SWAP-NAS]]: 报告 regularized SWAP 在多个空间上的 Spearman 提升。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Kendall's Tau]]

