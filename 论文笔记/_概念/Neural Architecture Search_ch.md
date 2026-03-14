---
type: concept
language: zh-CN
source_concept_note: "[[Neural Architecture Search]]"
aliases: [神经架构搜索, NAS]
---

# Neural Architecture Search 中文条目

## 一句话直觉
Neural Architecture Search（NAS）就是“让算法自动设计网络结构”，而不是完全靠人工试错。

## 它为什么重要
人工设计网络成本高、迁移慢，NAS 能在给定算力预算下更系统地探索高质量结构。

## 一个小例子
传统做法可能手工组合卷积层；NAS 会在候选操作里自动组合并比较，最终保留验证集表现最好的结构。

## 更正式的定义
NAS 是在定义好的搜索空间里，通过某种搜索策略（进化、强化学习、梯度法）和评估策略（全训练、权重共享、代理模型）来优化网络结构的过程。

## 核心要点
1. NAS 三要素：搜索空间、搜索策略、性能评估。
2. 真正的瓶颈通常是搜索成本。
3. 工程上常用近似评估换取速度。

## 这篇论文里怎么用
- [[LLMENAS]]: 在 NAS 框架中使用 LLM 引导进化算子，提高候选架构生成质量。

## 代表工作
- [[DARTS]]: 可微分 NAS。
- [[AmoebaNet]]: 经典进化 NAS。

## 相关概念
- [[Evolutionary Neural Architecture Search]]
- [[One-shot NAS]]
- [[Surrogate Predictor]]


## 补充（2026-03-14）
- [[AZ-NAS]]: 该论文使用 training-free 的多代理进化搜索框架。
