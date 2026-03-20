---
type: concept
language: zh-CN
source_concept_note: "[[Fisher Pruning]]"
aliases: [费舍尔剪枝, 基于费舍尔信息的剪枝]
---

# Fisher Pruning 中文条目

## 一句话直觉

Fisher Pruning 不问“这个通道数值大不大”，而是问“删掉它以后任务损失会涨多少”。

## 它为什么重要

这让剪枝决策直接和模型输出质量绑定，比只看权重范数或平均激活更贴近任务目标，尤其适合追求真实加速的通道剪枝。

## 一个小例子

两个通道平均激活都不高，但其中一个一旦删除就会明显改变 saliency 分布，另一个几乎没影响。Fisher Pruning 会优先保留前者、删除后者。

## 更正式的定义

Fisher Pruning 用局部二阶损失近似来估计删除某个参数或 feature map 的代价，并用经验 [[Fisher Information Matrix]] 近似其中的曲率项。

## 数学形式（如有必要）

常见的 feature-level 分数写成：

`Delta_k ~= (1 / 2N) * sum_n g_nk^2`

其中 `g_nk` 是第 `n` 个样本对第 `k` 个可剪单元或其 mask 的梯度。

## 核心要点

1. 它是基于梯度的任务敏感型剪枝，不同于纯幅值启发式。
2. 当目标是部署加速时，通常以 channel / feature-map 为单位使用。
3. 它可以和计算代价正则联合，直接做速度-精度折中优化。

## 这篇论文里怎么用

- [[Faster gaze prediction with dense networks and Fisher pruning]]: 用 Fisher Pruning 删除 saliency 模型中的 feature map，并同时考虑 FLOPs 下降。

## 代表工作

- [[Faster gaze prediction with dense networks and Fisher pruning]]: 给出更有原则的经验 Fisher 推导。
- Molchanov et al. (ICLR 2017): 与之非常接近的 CNN 梯度剪枝方法。

## 相关概念

- [[Fisher Information Matrix]]
- [[Knowledge Distillation]]
- [[Saliency Prediction]]

