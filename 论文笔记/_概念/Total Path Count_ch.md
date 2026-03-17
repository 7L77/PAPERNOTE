---
type: concept
language: zh-CN
source_concept_note: "[[Total Path Count]]"
aliases: [总路径计数, Total Path Count]
---

# Total Path Count 中文条目

## 一句话直觉

Total Path Count（TPC）是在不训练模型的前提下，用“输入到输出可形成多少条有效路径”来近似衡量架构表达能力。

## 它为什么重要

它计算快、只依赖结构参数，适合 zero-shot NAS 在大搜索空间中快速筛选候选。

## 一个小例子

若每层都能把输入分流到更多分支，那么多层叠加后端到端路径数会呈乘法增长，通常意味着更高表达容量。

## 更正式的定义

TPC 分数由各层路径计数组合而成。为避免数值过大，实践中常对每层路径数取对数后求和。

## 数学形式（如有必要）

\[
S_t = \sum_p \log(O_p)
\]

其中 \(O_p\) 为第 \(p\) 层路径计数。

## 核心要点

1. TPC 是结构代理，不依赖训练过程。
2. 它更偏向表达性，不直接等同泛化能力。
3. 适合作为搜索前期粗筛信号。

## 这篇论文里怎么用

- [[GEN-TPC-NAS]]: 第一阶段按 TPC 排序，第二阶段把 TPC 作为最低门槛后再看 Entropy。

## 代表工作

- [[TPC-NAS]]: 基于 TPC 的 zero-shot 架构搜索方法。

## 相关概念

- [[Network Expressivity]]
- [[Zero-Cost Proxy]]

