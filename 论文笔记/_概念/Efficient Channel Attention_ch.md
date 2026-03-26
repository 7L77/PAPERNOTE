---
type: concept
language: zh-CN
source_concept_note: "[[Efficient Channel Attention]]"
aliases: [高效通道注意力, Efficient Channel Attention]
---

# Efficient Channel Attention 中文条目

## 一句话直觉

ECA 是一种“低开销通道注意力”：通过通道向量上的小卷积直接学权重，不走重型 MLP。

## 它为什么重要

在 NAS 或鲁棒训练里，额外模块太重会放大训练成本。ECA 兼顾效果和效率，常用于特征融合阶段。

## 一个小例子

正常分支和鲁棒分支拼接后，ECA 会自动强调更有用的通道，抑制冗余或不稳定通道。

## 更正式的定义

对 \(U\in\mathbb{R}^{C\times H\times W}\)：
\[
z=\mathrm{GAP}(U),\quad
w=\sigma(\mathrm{Conv1D}(z)),\quad
F=w\odot U
\]

## 数学形式（如有必要）

ECA 的核心是“局部通道交互 + 轻量参数化”。

## 核心要点

1. 模块轻量，训练负担小。
2. 能提升通道级特征选择能力。
3. 适合放在鲁棒融合阶段。

## 这篇论文里怎么用

- [[RDNAS]]: 在双分支融合处使用 ECA，提升 clean 与 robust 表征协同效果。

## 代表工作

- [[RDNAS]]: 消融显示带 ECA 的双分支配置优于不带 ECA。

## 相关概念

- [[Attention Map]]
- [[Adversarial Robustness]]
