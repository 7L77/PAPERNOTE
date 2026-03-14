---
type: concept
language: zh-CN
source_concept_note: "[[One-shot NAS]]"
aliases: [一次训练 NAS, 权重共享 NAS]
---

# One-shot NAS 中文条目

## 一句话直觉
先训练一个“超级网络”，再把候选架构当成它的子网络快速评估，不用每个候选都从头训练。

## 它为什么重要
把 NAS 的搜索成本从“不可承受”降到“可实用”，是大规模搜索常见加速方案。

## 一个小例子
超级网络包含多种算子分支；评估某个候选时只激活对应路径，直接复用共享权重打分。

## 更正式的定义
One-shot NAS 是一种权重共享搜索范式：候选架构被视为同一 supernet 的子结构，通过共享参数近似评估性能。

## 核心要点
1. 速度快，但有共享权重偏差。
2. 子网络排序不一定等价于完整训练后的排序。
3. 常与代理模型或重排序策略联合使用。

## 这篇论文里怎么用
- [[LLMENAS]]: 作为搜索环路中的快速评估模块，降低候选评估开销。

## 代表工作
- [[ENAS]]: 参数共享 NAS 代表作。
- [[DARTS]]: 可微 NAS 与共享权重实践。

## 相关概念
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
- [[Evolutionary Neural Architecture Search]]

