---
type: concept
language: zh-CN
source_concept_note: "[[LayerCAM]]"
aliases: [分层类激活图, Layer-wise CAM]
---

# LayerCAM 中文条目

## 一句话直觉
LayerCAM 通过梯度给中间层特征图加权，显示模型做分类时“看了图像的哪里”。

## 它为什么重要
它能帮助我们比较 clean 与 adversarial 输入下注意区域的偏移，适合做鲁棒性诊断。

## 一个小例子
若干净样本关注物体中心，但对抗样本关注边缘，说明攻击成功改变了模型决策依据。

## 更正式的定义
LayerCAM 是一种类激活可视化方法，在中间层特征图上结合正梯度生成空间相关性热图，用于解释分类决策。

## 核心要点
1. 可在不同层级观察决策区域。
2. 适合做“前后差分”分析（如 clean vs adversarial）。
3. 可视化是诊断证据，不等同于严格因果结论。

## 这篇论文里怎么用
- [[Padding-Robustness Interplay]]: 用 LayerCAM 对比攻击前后解释图，分析不同 padding 下注意力向边界迁移的程度。

## 代表工作
- [[LayerCAM]]: Exploring hierarchical class activation maps for localization.

## 相关概念
- [[Adversarial Robustness]]
- [[Convolutional Padding]]

