---
type: concept
language: zh-CN
source_concept_note: "[[Hardware-aware NAS]]"
aliases: ["硬件感知 NAS", "Hardware-aware NAS"]
---

# Hardware-aware NAS 中文条目

## 一句话直觉

Hardware-aware NAS 不是只找最准的网络，而是找“精度和设备代价一起看起来最合适”的网络。

## 它为什么重要

部署时真正约束模型的往往是 latency、energy、memory，而不是论文里的单一 accuracy。

## 一个小例子

在 Jetson TX2 上，稍微差一点点精度但延迟只有一半的模型，可能比最准确的模型更有实际价值。

## 更正式的定义

Hardware-aware NAS 是把硬件指标或硬件约束显式纳入搜索目标的 NAS 问题，要求同时优化任务性能和设备侧效率。

## 核心要点

1. 精度和硬件效率必须联合考虑。
2. 看 Pareto 前沿通常比只看单分数更合理。
3. 一般既需要 accuracy 侧 proxy，也需要硬件性能预测器。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 在 energy 和 latency 约束下分析 zero-shot proxy 与真实 Pareto front 的偏差。

## 代表工作

- [[Zero-shot NAS Survey]]: 讨论 zero-shot NAS 在硬件约束场景下的表现。
- [[HW-NAS-Bench]]: 常见硬件感知 NAS benchmark。

## 相关概念

- [[Hardware Performance Model]]
- [[Pareto Frontier]]

