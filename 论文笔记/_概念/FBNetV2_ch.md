---
type: concept
language: zh-CN
source_concept_note: "[[FBNetV2]]"
aliases: [FBNetV2, 硬件感知可微 NAS]
---

# FBNetV2 中文条目

## 一句话直觉

FBNetV2 是一套“搜索时就考虑效率”的可微 NAS 框架。

## 它为什么重要

很多 NAS 方法只在搜索后再做压缩，FBNetV2 直接把效率项放进搜索目标，更贴近部署需求。

## 一个小例子

同一层有多个通道/结构选项，训练时先软组合，目标同时考虑分类损失和延迟/FLOPs 代价。

## 更正式的定义

面向移动端/边缘部署的硬件感知可微超网搜索方法。

## 数学形式（如有必要）

常见目标:
`L_total = L_task + lambda * L_efficiency`。

## 核心要点

1. 搜索期显式优化效率。
2. 软架构参数可后续离散化。
3. 对资源受限部署场景友好。

## 这篇论文里怎么用
- [[RNAS-CL]]: 采用 FBNetV2 风格的通道搜索与延迟约束设计。

## 代表工作

- FBNetV2 (Wan et al., 2020): 硬件感知可微 NAS 代表工作。

## 相关概念

- [[Neural Architecture Search]]
- [[Gumbel-Softmax]]
