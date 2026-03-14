---
type: concept
language: zh-CN
source_concept_note: "[[Knowledge Distillation]]"
aliases: [知识蒸馏, KD]
---

# Knowledge Distillation 中文条目

## 一句话直觉

知识蒸馏是让小模型向大模型“学答案分布和中间表示”，从而在更小参数下保留能力。

## 它为什么重要

在轻量模型场景里，蒸馏常常是“体积更小但精度不掉太多”的关键手段。

## 一个小例子

学生模型不只学 one-hot 标签，还学习教师 logits 与中间层特征，这样更容易逼近教师行为。

## 更正式的定义

知识蒸馏通过教师-学生框架，把教师模型的输出概率或隐藏表示作为额外监督信号。

## 数学形式（如有必要）

常见损失可写为
`L = alpha * L_task + beta * L_distill`，
其中 `L_distill` 可由 logits 对齐和中间层 MSE 组成。

## 核心要点

1. 蒸馏可以同时约束输出层与中间层。
2. 它广泛用于压缩与轻量模型训练。
3. 层对齐方式与损失权重会显著影响效果。

## 这篇论文里怎么用

- [[W-PCA]]: 搜索后训练阶段采用 EfficientBERT 风格 KD 损失（attention/hidden/embedding/prediction）。

## 代表工作

- EfficientBERT (Dong et al., 2021): 在轻量 BERT 搜索与训练中系统使用蒸馏。

## 相关概念

- [[Training-free NAS]]
- [[Neural Architecture Search]]
