---
type: concept
language: zh-CN
source_concept_note: "[[KL Divergence]]"
aliases: [KL 散度, Kullback-Leibler 散度]
---

# KL Divergence 中文条目

## 一句话直觉

KL 散度衡量“分布 P 和分布 Q 有多不一样”。

## 它为什么重要

蒸馏和鲁棒训练里，经常需要对齐两个预测分布，KL 是最常用度量之一。

## 一个小例子

教师和学生类别概率越接近，KL 越小；差异越大，KL 越大。

## 更正式的定义

`KL(P||Q) = sum_i P(i) log(P(i)/Q(i))`。

## 数学形式（如有必要）

KL 非负，且仅当 `P=Q`（几乎处处）时为 0。

## 核心要点

1. KL 是非对称的。
2. 当 Q 对某事件给极小概率时，KL 会变大。
3. 在 KD/TRADES 等目标里非常常见。

## 这篇论文里怎么用
- [[RNAS-CL]]: 在搜索与训练目标里都包含 student-teacher 输出分布 KL 项。

## 代表工作

- [[RNAS-CL]]: 在鲁棒 NAS 蒸馏目标中使用 KL。

## 相关概念

- [[Knowledge Distillation]]
- [[TRADES]]
