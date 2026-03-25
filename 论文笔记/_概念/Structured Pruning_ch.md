---
type: concept
language: zh-CN
source_concept_note: "[[Structured Pruning]]"
aliases: [结构化剪枝, 架构级剪枝]
---

# Structured Pruning 中文条目

## 一句话直觉
结构化剪枝不是“把零散权重置零”，而是直接删除有结构意义的模块（层、头、通道），所以模型天然更小、更快。

## 为什么重要
这类剪枝通常更容易转化为真实推理加速，因为硬件和推理引擎更容易利用“形状变小”的模型。

## 小例子
在 Transformer 里删除若干 MLP 通道和部分 block，参数量和 FLOPs 会同步下降，不依赖稀疏算子加速。

## 定义
Structured Pruning 指按结构单元成组删除参数的压缩方法，常见粒度包括层、注意力头、通道等。

## 关键点
1. 它会改变模型拓扑，而不只是改权重值。
2. 实际部署加速通常优于非结构化稀疏。
3. 但对功能破坏也更明显，需要更强的全局打分指标。

## 在本文中的作用
- [[TraceNAS]] 将结构化剪枝建模为联合深度-宽度搜索，并用梯度轨迹对齐评估候选可恢复性。

## 代表工作
- [[TraceNAS]]: 训练自由 NAS 搜索非均匀结构化剪枝 LLM。
- [[LLM-Pruner]]: 面向 LLM 的代表性结构化剪枝方法。

## 相关概念
- [[Channel Pruning]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
