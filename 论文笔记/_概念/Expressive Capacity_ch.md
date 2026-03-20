---
type: concept
language: zh-CN
source_concept_note: "[[Expressive Capacity]]"
aliases: ["表达能力", "Expressive Capacity"]
---

# Expressive Capacity 中文条目

## 一句话直觉

Expressive Capacity 说的是一个网络“能表示多复杂的函数、多复杂的决策边界”。

## 它为什么重要

如果架构本身表达能力不够，再好的优化器也很难把任务做好；很多 proxy 其实都在间接测这一点。

## 一个小例子

更深或更宽的 ReLU 网络通常能把输入空间切成更多线性区域，因此能表示更复杂的模式。

## 更正式的定义

Expressive Capacity 是神经网络架构表示复杂输入输出映射的能力。

## 核心要点

1. 表达能力高不代表训练一定顺利，也不代表泛化一定好。
2. linear regions、Jacobian 相关 proxy 往往在试图刻画这件事。
3. 好网络通常需要表达能力、可训练性、泛化能力一起成立。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 把它列为好 proxy 必须尽量覆盖的三个核心维度之一。

## 代表工作

- [[Zero-shot NAS Survey]]: 用它解释多类 proxy 的理论动机。
- [[Zen-NAS]]: survey 将其视为 expressivity 相关 proxy。

## 相关概念

- [[Trainability]]
- [[Generalization Capacity]]

