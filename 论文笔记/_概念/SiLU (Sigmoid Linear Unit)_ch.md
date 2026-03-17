---
type: concept
language: zh-CN
source_concept_note: "[[SiLU (Sigmoid Linear Unit)]]"
aliases: [SiLU, Swish]
---

# SiLU (Sigmoid Linear Unit) 中文条目

## 一句话直觉
SiLU 是一种更平滑的激活函数，保留了负区间的小幅连续响应。

## 它为什么重要
在对抗训练里，平滑梯度有时更容易优化，鲁棒表现也更稳定。

## 一个小例子
`x=-0.1` 时 ReLU 输出 0，而 SiLU 仍是一个小负值，不会完全断梯度。

## 更正式的定义

$$
\text{SiLU}(x)=x\cdot \sigma(x)
$$

## 核心要点
1. 非参数激活，无需额外学习参数。
2. 梯度连续，优化更平滑。
3. 在鲁棒 CNN 中常优于 ReLU。

## 这篇论文里怎么用
- [[Robust Principles]]: 将 ReLU 全部替换为 SiLU，得到显著鲁棒提升。

## 代表工作
- [[Robust Principles]]: 在对抗鲁棒语境下系统比较并推荐 SiLU。

## 相关概念
- [[GELU]]
- [[Adversarial Robustness]]

