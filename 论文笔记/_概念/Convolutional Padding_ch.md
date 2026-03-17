---
type: concept
language: zh-CN
source_concept_note: "[[Convolutional Padding]]"
aliases: [卷积填充, Conv Padding]
---

# Convolutional Padding 中文条目

## 一句话直觉
Convolutional Padding 是在卷积前给特征图四周补边界，用来控制输出尺寸和边缘信息处理方式。

## 它为什么重要
padding 不只是“凑尺寸”，还会改变模型在图像边界处看到的统计模式，进而影响泛化与鲁棒性。

## 一个小例子
32x32 输入配 3x3 卷积时，不加 padding 输出 30x30；padding=1 可保持 32x32。

## 更正式的定义
Padding 是卷积前对输入张量做边界扩展的算子。常见模式有 zero、reflect、replicate、circular。

## 核心要点
1. padding mode 会改变边界区域的特征分布。
2. 同一网络在不同 padding 下鲁棒性可明显不同。
3. padding 选择同时影响精度与运行开销。

## 这篇论文里怎么用
- [[Padding-Robustness Interplay]]: 把 padding mode 和 size 作为核心变量系统评估。

## 代表工作
- [[On the Interplay of Convolutional Padding and Adversarial Robustness]]: 专门研究 padding 与对抗鲁棒性的关系。

## 相关概念
- [[Adversarial Robustness]]
- [[AutoAttack]]

