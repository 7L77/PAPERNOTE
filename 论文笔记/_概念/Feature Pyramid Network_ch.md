---
type: concept
language: zh-CN
source_concept_note: "[[Feature Pyramid Network]]"
aliases: [特征金字塔网络, FPN]
---

# Feature Pyramid Network 中文条目

## 一句话直觉

Feature Pyramid Network 会把不同分辨率的特征拼成一个多尺度金字塔，让检测器同时看清大目标和小目标；但一旦要剪枝，这些跨尺度分支就会带来复杂耦合。

## 它为什么重要

很多检测模型的 neck 都是 FPN 风格。如果剪枝时忽略这些跨层、跨分支连接，FLOPs 可能降了，但 detector 的真实速度和结构可部署性未必会跟上。

## 一个小例子

检测器常会把浅层高分辨率特征和深层低分辨率特征融合成 `P3` 到 `P7`。这时删掉某条分支中的通道，往往会同时影响 lateral path 和 top-down path。

## 更正式的定义

FPN 是一种多尺度特征聚合架构，通过 bottom-up、lateral 和 top-down 路径在多个分辨率上构造语义较强的特征表示。

## 核心要点

1. 它是目标检测中非常常见的 neck 设计。
2. 它天然会引入跨分支耦合。
3. 想做有效剪枝，必须同时考虑 backbone、pyramid 和 detection head 的交互。

## 这篇论文里怎么用

- [[Group Fisher Pruning]]: 用 layer grouping 处理 FPN 与检测 head 之间的耦合通道，从而把结构化剪枝推广到 RetinaNet、FSAF、ATSS、PAA、Faster R-CNN 等检测模型。

## 代表工作

- [[Group Fisher Pruning]]: 把结构化剪枝从简单分类 backbone 推进到 FPN 检测器。

## 相关概念

- [[Coupled Channels]]
- [[Channel Pruning]]
- [[Group Convolution]]
