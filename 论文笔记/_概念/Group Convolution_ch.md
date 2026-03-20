---
type: concept
language: zh-CN
source_concept_note: "[[Group Convolution]]"
aliases: [分组卷积, GConv]
---

# Group Convolution 中文条目

## 一句话直觉

Group Convolution 会把通道切成若干组，每组只和自己内部的通道做卷积；这样更省算力，但也让“删通道”这件事不再是完全独立的。

## 它为什么重要

ResNeXt、RegNet 等网络大量使用分组卷积。若按普通卷积那套思路随便剪单个通道，很容易破坏组结构，或者剪了 FLOPs 却拿不到真实收益。

## 一个小例子

假设一个卷积有 64 个输入通道、4 个 group，那么每组处理 16 个通道。此时删除某个通道通常不能只看它自己，还要考虑整个组的结构一致性。

## 更正式的定义

分组卷积是一种把输入通道和输出通道划分为多个组，并让每个组独立完成卷积计算的算子。

## 核心要点

1. 它比普通 dense convolution 连接更稀疏。
2. 它会改变“什么才是合法的剪枝单位”。
3. 它常常导致层内通道耦合。

## 这篇论文里怎么用

- [[Group Fisher Pruning]]: 把 group conv 的输入/输出通道视作耦合结构，通过共享 mask 梯度来计算组重要性。

## 代表工作

- [[Group Fisher Pruning]]: 展示了如何在不破坏结构一致性的前提下剪 GConv。

## 相关概念

- [[Channel Pruning]]
- [[Depth-wise Convolution]]
- [[Coupled Channels]]
