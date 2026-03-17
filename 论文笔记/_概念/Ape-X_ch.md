---
type: concept
language: zh-CN
source_concept_note: "[[Ape-X]]"
aliases: [Ape-X, 分布式优先经验回放]
---

# Ape-X 中文条目

## 一句话直觉
Ape-X 是一种分布式强化学习训练范式: 多个 actor 并行采样，中心 learner 从优先经验回放中更新网络。

## 它为什么重要
它显著提高经验采集吞吐量，适合大规模 RL 训练任务。

## 一个小例子
不是单线程采样，而是几十个 worker 同时与环境交互，把样本送入共享 replay buffer。

## 更正式的定义
Ape-X (Horgan et al., 2018) 是面向 value-based RL 的分布式训练架构，结合异步 actor 与 centralized prioritized replay learner。

## 数学形式（如有必要）
优先采样概率常写为:
`P(i) = p_i^alpha / sum_k p_k^alpha`
并用 `beta` 做重要性采样修正。

## 核心要点
1. 并行 actor 提高采样速度。
2. learner 在中心侧从 replay 中持续更新。
3. 吞吐高，但样本效率不一定最佳。

## 这篇论文里怎么用
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: 使用 Ape-X 风格训练 RL-NAS agent，并在不同任务间做参数迁移。

## 代表工作
- Horgan et al., 2018 (Ape-X)
- Schaul et al., 2016 (Prioritized Experience Replay)

## 相关概念
- [[Reinforcement Learning]]
- [[Prioritized Experience Replay]]

