---
type: concept
language: zh-CN
source_concept_note: "[[Gumbel-Softmax]]"
aliases: [Gumbel-Softmax, 可微离散采样]
---

# Gumbel-Softmax 中文条目

## 一句话直觉

Gumbel-Softmax 让“本来离散不可导的选择”在训练时可导，最后再变成硬选择。

## 它为什么重要

NAS 里很多决策（选操作、选通道、选连接）本质离散，直接 argmax 不能反传。

## 一个小例子

先对 4 个通道选项学 soft 权重，训练后期温度降低，权重会接近 one-hot。

## 更正式的定义

对 logits 加 Gumbel 噪声并除温度做 softmax，形成可导近似分类采样。

## 数学形式（如有必要）

`y_i = exp((v_i+g_i)/tau) / sum_j exp((v_j+g_j)/tau)`，
`tau -> 0` 时接近离散 argmax。

## 核心要点

1. 连接离散搜索与梯度优化。
2. 温度退火决定软硬程度。
3. 常见做法是搜索期 soft、离散化期 hard。

## 这篇论文里怎么用
- [[RNAS-CL]]: 同时用于 tutor 层选择和通道搜索。

## 代表工作

- Jang et al. (2017): 提出 Gumbel-Softmax。
- [[RNAS-CL]]: 将其用于鲁棒 NAS 跨层蒸馏。

## 相关概念

- [[Neural Architecture Search]]
- [[Cross-Layer Knowledge Distillation]]
