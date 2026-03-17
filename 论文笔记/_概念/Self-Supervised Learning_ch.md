---
type: concept
language: zh-CN
source_concept_note: "[[Self-Supervised Learning]]"
aliases: [自监督学习, Self-Supervised Learning]
---

# Self-Supervised Learning 中文条目

## 一句话直觉

自监督学习（SSL）是在没有人工标签时，利用数据本身构造训练目标来学习通用表示。

## 它为什么重要

它能显著降低标注成本，并提升模型在低标注下游任务上的可迁移性与泛化能力。

## 一个小例子

在图像里随机遮住一些 patch，让模型预测被遮住的内容。被遮住区域就是“自动生成的监督信号”。

## 更正式的定义

Self-Supervised Learning 是一种表示学习范式：监督目标来自数据内在结构（如掩码重建、对比预测、时序预测），而非人工标注。

## 核心要点

1. 训练目标由数据自动构造，不依赖外部标签。
2. 常先进行大规模预训练，再做下游微调。
3. 在低标注场景尤其实用。

## 这篇论文里怎么用

- [[GEN-TPC-NAS]]: 搜索后使用 SSL 预训练，并提出 Entropy 代理来估计低标注泛化潜力。

## 代表工作

- [[MAE]]: 通过掩码重建学习视觉表示。
- [[MaskTAS]]: 在 Transformer NAS 中结合 SSL。

## 相关概念

- [[Masked Image Modeling]]
- [[Zero-Cost Proxy]]

