---
type: concept
language: zh-CN
source_concept_note: "[[Robust Search Primitive]]"
aliases: [鲁棒搜索基元, RSP]
---

# Robust Search Primitive 中文条目

## 一句话直觉
鲁棒搜索基元是指在“相邻架构比较”里，随着鲁棒性提升而稳定出现的 `(边, 操作)` 结构单元。

## 它为什么重要
它把 robust NAS 从“只看最终指标”的黑盒方式，变成“能指认具体结构元素”的可解释方式。

## 一个小例子
若 `A_{i+1}` 比 `A_i` 更鲁棒，且两者仅差一个基元，则该差异基元是鲁棒候选。

## 更正式的定义
在 REP 中，通过相邻架构与鲁棒性趋势构建 `B1/B2`，再取交集获得鲁棒基元集合。

## 核心要点
1. 基元级分析比整架构比较更细粒度。
2. 相邻比较能减少“变化太多导致归因困难”的问题。
3. 鲁棒基元是搜索先验，不是唯一可选基元。

## 这篇论文里怎么用
- [[REP]] 用该集合构造 `alpha_R`，并通过距离正则增强其选中概率。

## 代表工作
- [[REP]]: 提出鲁棒基元采样与概率增强搜索。

## 相关概念
- [[Robust Neural Architecture Search]]
- [[Probability Enhancement Search Strategy]]
- [[Cell-based Search Space]]
- [[Adversarial Robustness]]

