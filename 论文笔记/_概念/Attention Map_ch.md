---
type: concept
language: zh-CN
source_concept_note: "[[Attention Map]]"
aliases: [注意力图, Activation Attention Map]
---

# Attention Map 中文条目

## 一句话直觉

注意力图就是“模型在看哪里”的空间热度表示。

## 它为什么重要

它把中间特征变成可解释的空间信息，便于做 teacher-student 对齐或可视化分析。

## 一个小例子

识别“汽车”时，注意力图通常亮在车身和轮胎附近，而不是背景天空。

## 更正式的定义

把 `C x H x W` 的特征图沿通道聚合，得到 `H x W` 的空间图。

## 数学形式（如有必要）

在 [[RNAS-CL]] 中:
`[F(A)]_{h,w} = sum_c A_{c,h,w}^2`。

## 核心要点

1. 注意力图是从特征推导出来的表示。
2. 聚合方式会影响最终图的分布。
3. 在蒸馏中可作为中间层监督信号。

## 这篇论文里怎么用
- [[RNAS-CL]]: 用注意力图距离约束学生层向所选 tutor 层靠近。

## 代表工作

- [[RNAS-CL]]: 把注意力图对齐纳入鲁棒 NAS 搜索损失。

## 相关概念

- [[Cross-Layer Knowledge Distillation]]
- [[Knowledge Distillation]]
