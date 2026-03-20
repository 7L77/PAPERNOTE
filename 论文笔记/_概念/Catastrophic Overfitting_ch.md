---
type: concept
language: zh-CN
source_concept_note: "[[Catastrophic Overfitting]]"
aliases: [灾难性过拟合, CO in FAT]
---

# Catastrophic Overfitting 中文条目

## 一句话直觉

在快速/单步对抗训练里，模型可能“看起来变强了”，但对强攻击（如 PGD）鲁棒性会突然塌陷。

## 它为什么重要

它会制造鲁棒性的假象，如果只看弱攻击指标，容易得出错误结论。

## 一个小例子

训练过程中 FGSM 准确率持续上升，但某个 epoch 之后 PGD 准确率突然大幅下降。

## 更正式的定义

Catastrophic Overfitting 指的是：在 fast adversarial training 中，模型对强攻击的鲁棒性发生突发性劣化的训练不稳定现象。

## 数学形式（如有必要）

实践上通常通过“弱攻击曲线与强攻击曲线明显背离”来检测。

## 核心要点

1. 在单步对抗训练中较常见。
2. 只监控 FGSM 不够，需同时监控 PGD/AA。
3. 样本筛选策略与训练动态会影响其发生概率。

## 这篇论文里怎么用

- [[VDAT]]: 作者报告其样本级筛选并未引入灾难性过拟合。

## 代表工作

- [[VDAT]]: 给出了相关可视化与实验观察。

## 相关概念

- [[Adversarial Training]]
- [[AutoAttack]]

