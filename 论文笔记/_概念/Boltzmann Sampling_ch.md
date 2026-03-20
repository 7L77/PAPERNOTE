---
type: concept
language: zh-CN
source_concept_note: "[[Boltzmann Sampling]]"
aliases: [玻尔兹曼采样, Softmax 采样]
---

# Boltzmann Sampling 中文条目

## 一句话直觉
Boltzmann 采样把“分数”变成“概率”：温度高时更均匀探索，温度低时更偏向高分选项。

## 为什么重要
它提供了一个平滑调节探索-利用权衡的机制，常用于 NAS 采样策略。

## 小例子
两个架构分数接近时，高温下都会被频繁采样；降温后高分架构会更常被选中。

## 定义
对奖励 `r_i`，采样概率为
\[
p_i = \frac{\exp(r_i/T)}{\sum_j \exp(r_j/T)}.
\]

## 核心要点
1. 温度 `T` 决定概率分布尖锐程度。
2. 温度退火策略会显著影响收敛行为。
3. 在超大平坦空间中，单纯 Boltzmann 仍可能效率不足。

## 在本文中的作用
- [[MCTS-Learned Hierarchy]] 只在树的兄弟节点内做 Boltzmann 采样（Eq.2），相比全空间采样更高效。

## 代表工作
- Cesa-Bianchi et al. (2017)
- Su et al. (2021a)

## 相关概念
- [[Monte-Carlo Tree Search]]
- [[Upper Confidence Bound (UCB)]]
- [[Neural Architecture Search]]
