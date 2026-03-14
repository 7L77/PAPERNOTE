---
type: concept
language: zh-CN
source_concept_note: "[[Normalized Discounted Cumulative Gain]]"
aliases: [归一化折损累计增益, nDCG]
---

# Normalized Discounted Cumulative Gain 中文条目

## 一句话直觉

nDCG 是一种“重头部位置”的排序指标：越好的项目排得越靠前，得分越高。

## 它为什么重要

NAS 里真正关心的是能不能尽快找到最优架构，而不是把所有候选的相对顺序都同等精确地排好。

## 一个小例子

两个排序的总体相关性接近，但其中一个把前两名好模型错排到后面，nDCG 会明显下降；而 KT/SPR 可能下降不明显。

## 更正式的定义

nDCG 是 DCG（折损累计增益）除以理想 DCG 的归一化结果，范围通常在 `[0,1]`。

## 数学形式（如有必要）

VKDNW 文中的定义（Sec. III, Eq. (14)）：

`nDCG_P = (1/Z) * sum_{j=1..P} (2^{acc_{k_j}} - 1) / log2(1+j)`。

其中 `P` 是只看前多少名，`Z` 是理想排序下的归一化常数。

## 核心要点

1. nDCG 对排名位置敏感，前几名权重更大。
2. 对“检索 top 候选”的任务更贴近实际目标。
3. `P` 应该与真实 shortlist 规模对齐。

## 这篇论文里怎么用

- [[VKDNW]]: 将 nDCG 引入 TF-NAS 评测，补足 KT/SPR 的盲点。

## 代表工作

- [[VKDNW]]: 通过 toy 例子和大规模实验展示 nDCG 的区分力。

## 相关概念

- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Fisher Information Matrix]]
