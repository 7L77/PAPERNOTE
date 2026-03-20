---
type: concept
language: zh-CN
source_concept_note: "[[Coupled Channels]]"
aliases: [耦合通道, Channel Coupling]
---

# Coupled Channels 中文条目

## 一句话直觉

Coupled Channels 指的是那些“不能各删各的”通道；网络结构把它们绑在一起了，删一个通常就得连着删另一些。

## 它为什么重要

现代 CNN 里有残差、group conv、多分支 head、FPN 等结构，真正合理的剪枝单位常常不是某一层里的单个通道，而是跨层的一组通道。

## 一个小例子

在残差块里，两条分支最后要做逐元素相加。如果一条分支删了第 5 个通道，另一条没有删，那么虽然数学图还可能凑出来，但很难落成一个真正紧凑、可部署的结构。

## 更正式的定义

耦合通道是指由于计算图连接关系、共享下游使用方式或 group/depth-wise convolution 等算子约束，必须同步做剪枝决策的一组通道。

## 核心要点

1. 耦合可以跨层发生，不只是单层内部。
2. 残差连接和检测器多分支结构很容易产生通道耦合。
3. 真正有效的 structured pruning 应该以整组耦合单元为对象。

## 这篇论文里怎么用

- [[Group Fisher Pruning]]: 用 layer grouping 自动从计算图中找出耦合通道，并让它们共享同一个 mask。

## 代表工作

- [[Group Fisher Pruning]]: 把耦合通道作为复杂 CNN 结构里的基本剪枝单位。

## 相关概念

- [[Channel Pruning]]
- [[Feature Pyramid Network]]
- [[Group Convolution]]
