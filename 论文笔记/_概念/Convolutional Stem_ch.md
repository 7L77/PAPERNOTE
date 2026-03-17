---
type: concept
language: zh-CN
source_concept_note: "[[Convolutional Stem]]"
aliases: [卷积 stem, Conv Stem]
---

# Convolutional Stem 中文条目

## 一句话直觉
`Convolutional Stem` 是模型最前面用卷积做特征提取和下采样的入口层，通常比一次性大步长切块更平滑。

## 它为什么重要
卷积 stem 具有重叠感受野，往往能减少首层的信息丢失，对鲁棒训练更友好。

## 一个小例子
`7x7 stride=2` 的 stem 再进入主干，通常比 `patch=4 stride=4` 的非重叠切分保留更多局部细节。

## 更正式的定义
在输入端采用卷积滑窗结构作为第一阶段表示学习模块，通常伴随较温和的下采样策略。

## 核心要点
1. 重叠卷积是关键收益来源之一。
2. 下采样步幅越激进，鲁棒性越可能受损。
3. 常和 postponed downsampling 联合设计。

## 这篇论文里怎么用
- [[Robust Principles]]: 作为三条核心原则之一，优于 patchify stem。

## 代表工作
- [[Robust Principles]]: 对 conv stem 进行了系统鲁棒实验对比。

## 相关概念
- [[Patchify Stem]]
- [[Adversarial Robustness]]

