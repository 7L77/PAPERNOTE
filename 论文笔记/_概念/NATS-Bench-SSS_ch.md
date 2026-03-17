---
type: concept
language: zh-CN
source_concept_note: "[[NATS-Bench-SSS]]"
aliases: [NATS-SSS, NATS-Bench 尺寸搜索空间]
---

# NATS-Bench-SSS 中文条目

## 一句话直觉
NATS-Bench-SSS 是一个以“网络尺寸变化”为核心的 NAS 基准空间，适合大规模、可复现地比较代理评分方法。

## 它为什么重要
它提供了大量候选架构及预计算性能，便于系统评估 training-free proxy 的相关性和搜索质量。

## 一个小例子
先对 1000 个候选打分，再直接查询基准精度计算 Pearson/Kendall，可快速验证代理有效性。

## 更正式的定义
NATS-Bench 是 NAS 基准集合；其中 SSS（size search space）关注网络规模相关的结构变化，并提供多数据集性能记录。

## 核心要点
1. 候选数量大，统计稳定性好。
2. 常用于 CIFAR-10 / CIFAR-100 / ImageNet16-120 评测。
3. 对比训练前代理时很常见。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 在 NATS-Bench-SSS 上报告了相关性、搜索精度与搜索时间。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[NAS-Bench-201]]
- [[Zero-Cost Proxy]]

