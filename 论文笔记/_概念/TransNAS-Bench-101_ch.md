---
type: concept
language: zh-CN
source_concept_note: "[[TransNAS-Bench-101]]"
aliases: [TransNAS101]
---

# TransNAS-Bench-101 中文条目

## 一句话直觉
TransNAS-Bench-101 把 NAS 评测从单一分类任务扩展到多任务场景，用来检验方法的跨任务泛化能力。

## 它为什么重要
很多代理在分类任务有效，但在分割等任务上会失效；该基准能暴露这种迁移差距。

## 一个小例子
同一代理在 OC（分类）上相关性高，在 SS（分割）上相关性下降，这能直接反映方法边界。

## 更正式的定义
TransNAS-Bench-101 提供 macro/micro 两类搜索空间，并在 Taskonomy 相关任务上给出预评测结果。

## 核心要点
1. 任务多样，不只看 Top-1。
2. 同时覆盖 macro 与 micro 结构空间。
3. 适合评估训练前代理跨任务稳健性。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 在 OC/SS 的 macro 与 micro 任务上评估相关性与最终表现。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]

