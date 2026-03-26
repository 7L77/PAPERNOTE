---
type: concept
language: zh-CN
source_concept_note: "[[NAS-Bench-Suite-Zero]]"
aliases: [NAS-Bench-Suite-Zero, 零成本NAS基准套件]
---

# NAS-Bench-Suite-Zero 中文条目

## 一句话直觉
NAS-Bench-Suite-Zero 是一个“训练自由代理分数表”，预先存好大量架构的零成本指标。

## 它为什么重要
它让我们能快速、可复现地比较不同 zero-cost proxy，而不必每次都重新计算。

## 一个小例子
需要 SynFlow 分数时，可直接查表，而不是对每个架构单独跑一次 SynFlow 计算。

## 更正式的定义
该基准套件汇总了多个搜索空间中大量架构的训练自由代理指标，服务于 proxy-based NAS 研究。

## 核心要点
1. 关注 training-free proxy 元数据。
2. 适合做目标函数与代理指标对比实验。
3. 节省算力并提升复现性。

## 这篇论文里怎么用
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 搜索阶段读取 SynFlow 分数作为训练自由目标。

## 代表工作
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 与 NAS-RobBench-201 联合使用，评估鲁棒 NAS 目标设计。

## 相关概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]

