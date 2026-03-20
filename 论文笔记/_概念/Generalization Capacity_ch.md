---
type: concept
language: zh-CN
source_concept_note: "[[Generalization Capacity]]"
aliases: ["泛化能力", "Generalization Capacity"]
---

# Generalization Capacity 中文条目

## 一句话直觉

Generalization Capacity 关心的是：网络在没见过的数据上还能不能表现好，而不是只在训练数据上看起来厉害。

## 它为什么重要

NAS 最终关心的是测试性能。只会训练集上好看的架构，并不是我们真正想找的架构。

## 一个小例子

两个网络都能把训练子集拟合得很好，但只有一个在验证集上继续保持高分，后者泛化能力更强。

## 更正式的定义

Generalization Capacity 是模型或架构在未见样本上保持性能的能力。

## 核心要点

1. 这是最难在初始化时可靠估计的性质之一。
2. 很多 zero-shot proxy 对它覆盖得很弱。
3. 同时包含可训练性与泛化性的 proxy 往往更有潜力。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 指出当前 proxy 的一个核心短板就是对泛化能力建模不足。

## 代表工作

- [[Zero-shot NAS Survey]]: 强调现有 proxy 普遍忽略这一维。
- [[ZiCo]]: 文中提到的一个可能更兼顾泛化与可训练性的方向。

## 相关概念

- [[Expressive Capacity]]
- [[Trainability]]

