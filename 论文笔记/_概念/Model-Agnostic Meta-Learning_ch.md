---
type: concept
language: zh-CN
source_concept_note: "[[Model-Agnostic Meta-Learning]]"
aliases: [MAML, 模型无关元学习]
---

# Model-Agnostic Meta-Learning 中文条目

## 一句话直觉
MAML 学的是“一个好初始化”，让模型在新任务上只用少量梯度步就能快速适配。

## 它为什么重要
在 few-shot 学习里，样本少、任务变化快，MAML 的目标正好是提升“快速适应能力”。

## 一个小例子
先在很多 5-way 小任务上元训练，遇到新 5-way 任务时，只更新 1-2 步就能达到不错精度。

## 更正式的定义
MAML 是双层优化：内层在 support 集更新参数，外层在 query 集最小化更新后的损失。

## 数学形式（如有必要）
`theta' = theta - alpha * grad_theta L_support(theta)`，
`min_theta sum_t L_query^t(theta'_t)`。

## 核心要点
1. 内层负责任务内适配，外层负责学习可适配初始化。
2. 原始形式含二阶梯度，计算相对重。
3. 是元学习领域最常见基线之一。

## 这篇论文里怎么用
- [[IBFS]]: 用 MAML 收敛分析支撑其“一阶 proxy 打分”路线。

## 代表工作
- Finn et al. (2017): MAML 原始论文。
- [[IBFS]]: 将该视角用于 few-shot NAS 排序。

## 相关概念
- [[Few-shot Learning]]
- [[Reptile]]
- [[Neural Tangent Kernel]]
