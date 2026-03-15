---
type: concept
language: zh-CN
source_concept_note: "[[Mixed-Rank Adapter]]"
aliases: [混合秩适配器, Mixed-Rank Adapter]
---

# Mixed-Rank Adapter 中文条目

## 一句话直觉
Mixed-Rank Adapter 让不同层可使用不同 rank，并把这些选择统一放进一个可搜索的超网里。

## 它为什么重要
统一 rank 往往不够灵活；混合秩能更细粒度地在参数量和精度之间做分配。

## 一个小例子
某些层只需要 rank 4 就够，另一些层需要 rank 16；混合秩能同时容纳这两类需求。

## 更正式的定义
Mixed-Rank Adapter 指在超网中编码多种 rank 选择，使导出的子网可拥有层级别的 rank 组合。

## 核心要点
1. 打破单一全局 rank 限制。
2. 适合 one-shot 权重共享训练。
3. 提供更丰富的 NAS 搜索空间。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 将 mixed-rank 作为核心设计，用于导出不同预算子网。

## 代表工作
- [[LLaMA-NAS]]: 基于 mixed-rank adapter 做 LLM 结构搜索。

## 相关概念
- [[Super-network]]
- [[Low-Rank Adapter]]
