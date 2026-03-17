---
type: concept
language: zh-CN
source_concept_note: "[[Actor-Critic Reinforcement Learning]]"
aliases: [A2C, 演员-评论家强化学习]
---

# Actor-Critic Reinforcement Learning 中文条目

## 一句话直觉

把强化学习拆成“做决策的人（actor）”和“打分的人（critic）”，让打分结果来指导策略更新。

## 它为什么重要

纯策略梯度噪声大、训练抖动明显；actor-critic 用价值函数做基线，通常更稳、更快收敛。

## 一个小例子

在 NAS 搜索里，actor 决定当前用“初始化/变异/交叉”哪种操作；critic 评估当前状态值。如果这次奖励高，actor 会在类似状态下更倾向同类操作。

## 更正式的定义

Actor-Critic 是一类联合学习策略函数和价值函数的强化学习方法：
- 策略 `pi_theta(a|s)` 负责采样动作；
- 价值函数 `V_psi(s)` 或 `Q_psi(s,a)` 负责提供优势估计；
- 最终用优势项更新策略参数。

## 数学形式（如有必要）

\[
\theta \leftarrow \theta + \eta \nabla_\theta \log \pi_\theta(a_t|s_t)\,\hat A_t
\]
\[
\hat A_t = r_t + \gamma V_\psi(s_{t+1}) - V_\psi(s_t)
\]

其中 `theta` 是 actor 参数，`psi` 是 critic 参数，`r_t` 是奖励，`gamma` 是折扣因子。

## 核心要点

1. actor 负责“选动作”，critic 负责“评好坏”。
2. 优势函数可显著降低策略梯度方差。
3. critic 拟合得好坏，直接影响整体训练稳定性。

## 这篇论文里怎么用

- [[APD]]: 用 actor-critic 学习 prompt 操作调度策略，驱动 proxy 进化过程。

## 代表工作

- [[Asynchronous Methods for Deep Reinforcement Learning]]: A3C 是经典 actor-critic 实践。
- [[Proximal Policy Optimization Algorithms]]: 工程中最常见的 actor-critic 优化范式之一。

## 相关概念

- [[LLM-guided Search]]
- [[Neural Architecture Search]]
- [[Training-free NAS]]

