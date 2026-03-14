---
type: concept
language: zh-CN
source_concept_note: "[[Weighted Response Correlation]]"
aliases: [加权响应相关性, WRCor]
---

# Weighted Response Correlation 中文条目

## 一句话直觉

`Weighted Response Correlation (WRCor)` 用“不同样本在网络各层响应是否足够不相似”来评估架构潜力，并给高层响应更大权重。

## 它为什么重要

WRCor 让我们在不训练候选模型的情况下完成架构排序，是 zero-shot NAS 中典型的低成本代理指标。

## 一个小例子

同一批样本下，若架构 A 的响应相关矩阵非对角元素普遍更小、架构 B 更大，那么 WRCor 通常认为 A 更优。

## 更正式的定义

WRCor 将激活与梯度响应相关矩阵按层加权求和，再取 log-det：

\[
S_{\text{WRCor}}=\log(\det(K)),
\quad
K=\sum_{l}\sum_{i}2^l\left(|C^{A}_{l,i}|+|C^{G}_{l,i}|\right)
\]

## 数学形式（如有必要）

- \(2^l\)：层权重，强调高层语义特征。
- \(|C|\)：相关系数绝对值。
- \(\log\det\)：将矩阵结构压缩为可比较标量分数。

## 核心要点

1. 同时刻画激活相关性和梯度相关性。
2. 通过层加权表达“高层更关键”的经验观察。
3. 可直接用于 NAS 搜索中的候选排序。

## 这篇论文里怎么用

- [[WRCor]]: 把 WRCor 作为主 proxy，并与其他 proxy 做投票（SPW/SJW）提升稳健性。

## 代表工作

- [[WRCor]]: 系统提出并验证 WRCor 在多个 benchmark 上的效果。

## 相关概念

- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Network Expressivity]]
- [[Spearman's Rank Correlation]]


