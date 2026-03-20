---
type: concept
language: zh-CN
source_concept_note: "[[Depth-wise Convolution]]"
aliases: [深度卷积, 深度可分离卷积中的 depth-wise 部分, DWConv]
---

# Depth-wise Convolution 中文条目

## 一句话直觉

Depth-wise Convolution 会给每个输入通道各配一个空间卷积核，而不是像普通卷积那样把所有通道密集混合起来；它很省算力，但结构约束也更强。

## 它为什么重要

MobileNet 这类轻量网络大量依赖 depth-wise convolution。一个剪枝方法如果只会处理普通卷积，就很难覆盖真正实用的移动端网络。

## 一个小例子

一个 32 通道的 depth-wise 层里，每个通道都有自己专属的空间卷积核。删掉某个通道，就等于把对应输入路径和那组卷积核一起删掉。

## 更正式的定义

Depth-wise convolution 是分组卷积的特例，其中 group 数等于输入通道数，因此每个输入通道都被独立卷积。

## 核心要点

1. 它可以看作 group convolution 的极端情况。
2. 它是轻量 CNN 的核心构件。
3. 对它做剪枝时必须尊重“一通道一组”的结构。

## 这篇论文里怎么用

- [[Group Fisher Pruning]]: 把 DWConv 纳入 layer grouping 与共享 mask 框架，使 MobileNetV2 也能做有效结构化剪枝。

## 代表工作

- [[Group Fisher Pruning]]: 在 MobileNetV2 上验证了 DWConv 场景下的方法有效性。

## 相关概念

- [[Group Convolution]]
- [[Channel Pruning]]
- [[Coupled Channels]]
