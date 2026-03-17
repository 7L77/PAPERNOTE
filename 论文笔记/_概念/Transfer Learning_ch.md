---
type: concept
language: zh-CN
source_concept_note: "[[Transfer Learning]]"
aliases: [迁移学习, Transfer Learning]
---

# Transfer Learning 中文条目

## 一句话直觉
迁移学习就是把源任务学到的参数或表示迁到目标任务上，减少从零开始的训练成本。

## 它为什么重要
在数据少、算力紧或训练很慢的场景下，迁移学习通常能更快收敛，并提升目标任务表现。

## 一个小例子
先在大规模通用图像上预训练，再在小规模专用数据上微调，通常比从零训练更稳更快。

## 更正式的定义
给定源任务 `Ts` 和目标任务 `Tt`，先得到源参数 `theta_s*`，再用其初始化目标模型并在 `Tt` 上继续优化。

## 数学形式（如有必要）
`theta_t(0) <- theta_s*`
`theta_t* = argmin_theta L_t(theta)`

## 核心要点
1. 迁移是否有效取决于源任务与目标任务相关性。
2. 可能出现负迁移（negative transfer）。
3. 微调层数和学习率策略是关键超参数。

## 这篇论文里怎么用
- [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]: 在 TransNAS-Bench-101 的任务对之间迁移 RL-NAS agent 参数，并比较 zero-shot、fine-tuning、re-training 三种 regime。

## 代表工作
- Pan and Yang, 2010 (survey)
- Yosinski et al., 2014 (feature transferability)

## 相关概念
- [[Reinforcement Learning]]
- [[Neural Architecture Search]]

