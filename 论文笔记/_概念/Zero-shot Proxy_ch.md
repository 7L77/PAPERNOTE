---
type: concept
language: zh-CN
source_concept_note: "[[Zero-shot Proxy]]"
aliases: ["零训练代理指标", "Zero-shot Proxy"]
---

# Zero-shot Proxy 中文条目

## 一句话直觉

Zero-shot Proxy 就是“拿来替代真实训练后精度的便宜分数”。

## 它为什么重要

没有 proxy，zero-shot NAS 就没有灵魂，因为整个流程就是靠它来决定哪些架构值得继续看。

## 一个小例子

如果某个候选网络在初始化时的 SNIP 分数明显高于另一个网络，搜索过程就可能直接优先保留它，而不训练两者。

## 更正式的定义

Zero-shot Proxy 是对未训练网络或随机初始化网络计算的廉价统计量，用来估计或排序其最终训练后的性能。

## 核心要点

1. proxy 真正重要的是排序是否靠谱，不是数值本身有多漂亮。
2. 不同 proxy 往往只覆盖表达性、可训练性、泛化性中的一部分。
3. 在 top-performing 高精度候选上失效，是很多 proxy 的共性问题。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 用统一 taxonomy 和大规模实验评测不同 proxy 的有效性。

## 代表工作

- [[Zero-shot NAS Survey]]: 系统综述与对比。
- [[Zen-NAS]]: 以 expressivity 为核心的 proxy 代表。

## 相关概念

- [[Zero-shot NAS]]
- [[Trainability]]

