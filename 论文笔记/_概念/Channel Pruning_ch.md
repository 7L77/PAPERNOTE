---
type: concept
language: zh-CN
source_concept_note: "[[Channel Pruning]]"
aliases: [通道剪枝, Structured Channel Pruning]
---

# Channel Pruning 中文条目

## 一句话直觉

Channel Pruning 就是“整根整根地删特征通道”，而不是零零散散地删权重；它关心的不只是参数变少，更关心网络能不能真的变窄、变快。

## 它为什么重要

很多稀疏化方法虽然让参数矩阵里多了很多零，但普通硬件上的 dense kernel 并不会因此自动更快。通道剪枝直接删整段通道，对部署更友好。

## 一个小例子

如果某个卷积层输出 64 个通道，其中 16 个通道几乎不影响最终预测，那么通道剪枝会把这 16 个通道整体删掉，后续层也不用再读取和处理它们。

## 更正式的定义

通道剪枝是一类结构化模型压缩方法，它删除整个 channel/filter 以及对应张量切片，同时保持网络仍然是一个合法的稠密结构。

## 核心要点

1. 它属于 structured pruning，不同于零散权重稀疏化。
2. 剪完之后通常还需要 fine-tune。
3. 能不能真正加速，取决于删掉的通道是否真的变成更小的 dense operator。

## 这篇论文里怎么用

- [[Group Fisher Pruning]]: 把通道剪枝推广到跨层耦合通道场景，让复杂结构里的剪枝也能落成有效的紧凑模型。

## 代表工作

- [[Group Fisher Pruning]]: 用 Fisher 重要性和 layer grouping 做全局贪心剪枝。

## 相关概念

- [[Coupled Channels]]
- [[Group Convolution]]
- [[Depth-wise Convolution]]
