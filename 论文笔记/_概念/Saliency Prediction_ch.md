---
type: concept
language: zh-CN
source_concept_note: "[[Saliency Prediction]]"
aliases: [显著性预测, 注视点预测, 视觉注意力预测]
---

# Saliency Prediction 中文条目

## 一句话直觉

Saliency Prediction 研究的是“给一张图，人更可能先看哪里”。

## 它为什么重要

它把人的视觉注意力变成可计算信号，可用于图像裁剪、视频压缩、界面设计、认知研究和下游视觉系统。

## 一个小例子

在街景图里，模型通常应该把较高概率分配给人脸、招牌文字或显眼物体，而不是平均分到所有像素。

## 更正式的定义

Saliency Prediction 以眼动 / fixation 数据为监督，学习图像像素上的人类注视概率分布。

## 数学形式（如有必要）

常见输出是归一化概率图 `Q(x, y | I)`，数值越高表示观察者越可能在该位置停留视线。

## 核心要点

1. 现代 saliency 模型常输出概率分布，而不是简单二值区域。
2. 常见指标包括 AUC、NSS、SIM、KL 等。
3. 数据集先验，尤其是 [[Center Bias]]，往往非常重要。

## 这篇论文里怎么用

- [[Faster gaze prediction with dense networks and Fisher pruning]]: 目标任务就是图像注视分布预测，并进一步压缩模型以获得更快推理。

## 代表工作

- DeepGaze I / II: 以分类预训练特征做 saliency prediction 的代表性强基线。
- [[Faster gaze prediction with dense networks and Fisher pruning]]: 用蒸馏和剪枝做高效 saliency 建模。

## 相关概念

- [[Center Bias]]
- [[Knowledge Distillation]]
- [[KL Divergence]]

