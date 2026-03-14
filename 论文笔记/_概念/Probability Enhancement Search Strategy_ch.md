---
type: concept
language: zh-CN
source_concept_note: "[[Probability Enhancement Search Strategy]]"
aliases: [概率增强搜索策略, PESS]
---

# Probability Enhancement Search Strategy 中文条目

## 一句话直觉
不硬性只选鲁棒基元，而是通过距离正则“提高其被选概率”，同时保留对自然精度有利的其他基元。

## 它为什么重要
在鲁棒性与自然精度之间建立可控折中，避免“只追鲁棒导致性能塌陷”。

## 一个小例子
同一条边上若有多个鲁棒候选操作，策略会同时提升它们概率，最终仍由验证损失决定谁胜出。

## 更正式的定义
在双层优化中最小化：
`L_val(w*(alpha), alpha) + lambda * ||alpha - alpha_R||^2`，
其中 `alpha_R` 是鲁棒基元指示矩阵。

## 核心要点
1. 这是“软偏置”而非“硬掩码”。
2. 距离项兼具正则化作用，可缓解架构参数过拟合验证集。
3. 与现有可微 NAS 主流程兼容，插件化集成成本低。

## 这篇论文里怎么用
- [[REP]] 在采样鲁棒基元后，默认使用欧氏距离做概率增强。

## 代表工作
- [[REP]]: 将该策略用于鲁棒可微 NAS。

## 相关概念
- [[Robust Search Primitive]]
- [[Robust Neural Architecture Search]]
- [[Neural Architecture Search]]

