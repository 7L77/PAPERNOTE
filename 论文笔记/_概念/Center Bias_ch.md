---
type: concept
language: zh-CN
source_concept_note: "[[Center Bias]]"
aliases: [中心偏置, 图像中心先验]
---

# Center Bias 中文条目

## 一句话直觉

人在看图时，天然更容易把视线落在图像中心附近，而不是边缘。

## 它为什么重要

很多 saliency 数据集都带有明显的中心注视趋势，所以如果模型不建模这个先验，即便视觉特征很强，指标也可能吃亏。

## 一个小例子

如果两件同样显眼的物体分别放在图像中央和边缘，真实 eye-tracking 数据里，中心那件通常会拿到更高 fixation 概率。

## 更正式的定义

Center Bias 是 fixation 位置的一个数据集级先验，用来描述观察者更倾向注视图像中心的统计事实。

## 数学形式（如有必要）

它常以 `log Q(x, y)` 这样的先验项加入最终 saliency 分布归一化之前。

## 核心要点

1. 它不只是模型偏差，也来自人类观看习惯与数据采集方式。
2. 不同数据集的中心偏置强度不一样。
3. 好的 saliency 模型通常同时结合内容线索和中心先验。

## 这篇论文里怎么用

- [[Faster gaze prediction with dense networks and Fisher pruning]]: 在最终 softmax 前加入数据集相关的对数中心先验。

## 代表工作

- DeepGaze 系列通常显式建模 center-bias。
- [[Faster gaze prediction with dense networks and Fisher pruning]]: 在压缩模型时仍保留这个关键先验。

## 相关概念

- [[Saliency Prediction]]
- [[KL Divergence]]
