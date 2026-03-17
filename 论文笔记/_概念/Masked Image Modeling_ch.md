---
type: concept
language: zh-CN
source_concept_note: "[[Masked Image Modeling]]"
aliases: [掩码图像建模, Masked Image Modeling]
---

# Masked Image Modeling 中文条目

## 一句话直觉

Masked Image Modeling（MIM）通过“遮住一部分图像再恢复”的任务，让模型在无标签条件下学到更有语义的表示。

## 它为什么重要

它是视觉 SSL 的核心预训练任务之一，在少标签微调时通常能带来更好的精度和稳定性。

## 一个小例子

把图像切成 patch，随机遮掉大部分 patch，让模型仅根据剩余可见区域重建被遮挡内容。

## 更正式的定义

MIM 是一种自监督目标：对输入图像 token/patch 做随机掩码，训练模型预测缺失信息（像素、特征或 token）。

## 核心要点

1. 掩码比例决定任务难度与表示学习压力。
2. 常用于预训练阶段，后续用下游任务微调。
3. 对低标注场景通常特别有效。

## 这篇论文里怎么用

- [[GEN-TPC-NAS]]: 在 ViT 评测阶段使用 MIM 预训练，再在低标注 ImageNet 上微调比较架构泛化能力。

## 代表工作

- [[MAE]]: 经典 MIM 框架。
- [[MaskTAS]]: 在 Transformer NAS 中结合 MIM 与蒸馏。

## 相关概念

- [[Self-Supervised Learning]]
- [[Zero-Cost Proxy]]

