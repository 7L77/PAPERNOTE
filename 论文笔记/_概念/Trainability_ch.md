---
type: concept
language: zh-CN
source_concept_note: "[[Trainability]]"
aliases: ["可训练性", "Trainability"]
---

# Trainability 中文条目

## 一句话直觉

Trainability 说的是一个网络“好不好训”，也就是梯度能不能顺、优化会不会卡住。

## 它为什么重要

表达能力再强，如果训练一开始就梯度爆炸、消失或极难优化，那个架构也很难真正跑出好结果。

## 一个小例子

如果一个网络在各层之间梯度传播稳定，而另一个网络很快出现梯度失真，前者通常更容易训练成功。

## 更正式的定义

Trainability 是网络架构支持稳定梯度传播、高效优化并收敛到好解的能力。

## 核心要点

1. 很多 gradient-based proxy 实际上主要在测可训练性。
2. 可训练性好不等于泛化一定好。
3. 拓扑、宽度、skip connection 都会显著影响可训练性。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 把它作为 proxy 设计的核心维度之一，并指出许多成功 proxy 主要抓住了这一面。

## 代表工作

- [[Zero-shot NAS Survey]]: 用它解释多类 gradient-based proxy 的有效性。
- [[How does topology influence gradient propagation and model performance of deep networks with DenseNet-type skip connections?]]: survey 引用的 topology-trainability 代表工作。

## 相关概念

- [[Expressive Capacity]]
- [[Generalization Capacity]]

