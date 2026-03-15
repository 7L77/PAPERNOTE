---
type: concept
language: zh-CN
source_concept_note: "[[Architecture Density]]"
aliases: [架构密度, 连接密度]
---

# Architecture Density 中文条目

## 一句话直觉
Architecture Density 衡量“架构图里有多少边被激活”；边越多，信息路径越丰富，在一些鲁棒场景下通常更抗攻击。

## 它为什么重要
它把“密连接更好”这种经验结论，变成可量化、可比较的结构指标。

## 一个小例子
同样 14 条候选边，一个架构激活 11 条，另一个只激活 6 条；前者密度更高，在 [[RobNet]] 的统计中通常鲁棒精度也更高。

## 更正式的定义
若总边数为 `|E|`，激活边数为 `|E_connected|`，则
\[
D=\frac{|E_{connected}|}{|E|}
\]
在 RobNet 的二值参数化下：
\[
D=\frac{\sum_{i,j,k}\alpha^{(i,j)}_k}{|E|}
\]
其中 `alpha` 表示某条边上的某操作是否被激活。

## 核心要点
1. 这是结构层面的指标，不依赖训练后权重值。
2. 在 RobNet 的样本中，密度与对抗精度呈正相关。
3. 它是诊断信号，不等价于严格鲁棒保证。

## 这篇论文里怎么用
- [[RobNet]]: 用架构密度解释“密连接模式更鲁棒”的经验规律。

## 代表工作
- [[RobNet]]: 在大量采样架构上验证了密度与鲁棒性的相关性。

## 相关概念
- [[Neural Architecture Search]]
- [[Cell-based Search Space]]
- [[Adversarial Robustness]]

