---
type: concept
language: zh-CN
source_concept_note: "[[Prioritized Experience Replay]]"
aliases: [优先经验回放, PER]
---

# Prioritized Experience Replay 中文条目

## 一句话直觉
优先经验回放不是均匀抽样历史数据，而是更常抽“更有学习价值”的样本（通常 TD 误差更大）。

## 它为什么重要
均匀回放会浪费更新在信息量低的样本上。PER 可以把更新预算集中到更关键的误差上。

## 一个小例子
某条 transition 的预测误差很大，重复学习它会更快修正价值估计偏差。

## 更正式的定义
PER 给每个样本 `i` 一个优先级 `p_i`，并按 `p_i` 的幂次分布进行采样，而不是均匀随机。

## 数学形式（如有必要）
采样概率:
`P(i) = p_i^alpha / sum_k p_k^alpha`
重要性采样权重:
`w_i = (1 / (N * P(i)))^beta`

## 核心要点
1. `alpha` 越大，优先采样越强。
2. `beta` 用于修正非均匀采样带来的估计偏差。
3. 误差估计噪声大时，PER 也可能引入不稳定性。

## 这篇论文里怎么用
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: 训练 RL-NAS agent 时使用 PER（容量 `25k`, `alpha=0.6`, `beta=0.4`）。

## 代表工作
- Schaul et al., 2016 (PER)
- Horgan et al., 2018 (Ape-X)

## 相关概念
- [[Ape-X]]
- [[Reinforcement Learning]]

