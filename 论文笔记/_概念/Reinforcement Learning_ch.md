---
type: concept
language: zh-CN
source_concept_note: "[[Reinforcement Learning]]"
aliases: [强化学习, Reinforcement Learning]
---

# Reinforcement Learning 中文条目

## 一句话直觉
强化学习就是让智能体在环境里“试错”，通过奖励信号学会长期更优的决策策略。

## 它为什么重要
很多问题是连续决策问题（例如架构搜索、控制、游戏），强化学习天然适合优化长期回报。

## 一个小例子
走迷宫时，只有到终点才给奖励。智能体会逐步学习哪些动作序列更容易到终点。

## 更正式的定义
强化学习通常建模为 MDP: 状态 `s`、动作 `a`、转移、奖励 `r`，目标是学习策略 `pi(a|s)` 来最大化累计回报。

## 数学形式（如有必要）
常用回报定义:
`G_t = sum_{k=0..infinity} gamma^k r_{t+k+1}`
其中 `gamma` 是折扣因子，控制远期奖励权重。

## 核心要点
1. 优化目标是长期收益，不是单步监督标签。
2. 需要平衡探索与利用。
3. 常见方法有 value-based 与 policy-based 两大类。

## 这篇论文里怎么用
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: 用 RL agent 来做 NAS 中的迭代架构编辑与评估决策。

## 代表工作
- DQN (Mnih et al., 2015)
- Ape-X (Horgan et al., 2018)

## 相关概念
- [[Ape-X]]
- [[Prioritized Experience Replay]]

