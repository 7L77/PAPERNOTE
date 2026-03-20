---
type: concept
language: zh-CN
source_concept_note: "[[Zero-shot NAS]]"
aliases: ["训练前 NAS", "Zero-shot NAS"]
---

# Zero-shot NAS 中文条目

## 一句话直觉

Zero-shot NAS 就是在“还没认真训练网络之前”，先用一个很便宜的初始化分数去近似判断架构好不好。

## 它为什么重要

NAS 最贵的部分通常是反复训练候选模型。只要这个便宜分数足够靠谱，就能把大量明显不行的候选先筛掉。

## 一个小例子

有 5000 个候选 CNN 时，不再把它们都训练一遍，而是先算 SNIP、Synflow、Zen-score 这类 proxy，只保留分数高的一小部分再做后续验证。

## 更正式的定义

Zero-shot NAS 是一种在搜索阶段尽量不训练候选网络、而是利用随机初始化时的 proxy 对架构进行排序或筛选的 NAS 范式。

## 核心要点

1. 它的核心优势是便宜，不是天然更准。
2. 成败几乎完全取决于 proxy 与最终精度的相关性。
3. 候选评估越贵，Zero-shot NAS 的价值越大。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 把 zero-shot NAS 当作全文主线，系统比较各类 proxy 的适用边界。

## 代表工作

- [[Zero-shot NAS Survey]]: 对 zero-shot NAS 的系统综述。
- [[Zero-Cost Proxies for Lightweight NAS]]: 早期代表性 zero-cost proxy 工作。

## 相关概念

- [[Zero-shot Proxy]]
- [[Hardware-aware NAS]]

