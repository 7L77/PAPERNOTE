---
type: concept
language: zh-CN
source_concept_note: "[[Reptile]]"
aliases: [Reptile, 一阶元学习]
---

# Reptile 中文条目

## 一句话直觉
Reptile 每次在一个任务上先做少量更新，再把全局初始化往“任务更新后的参数”方向拉近。

## 它为什么重要
它不需要二阶梯度，计算和实现都更轻量，常用于 few-shot 元学习基线。

## 一个小例子
采样任务 `t`，在 support 集上更新几步得到 `phi_t`，然后做 `theta <- theta + epsilon*(phi_t-theta)`。

## 更正式的定义
Reptile 通过一阶近似，把元学习目标转化为对多任务快速适配方向的平均更新。

## 数学形式（如有必要）
`theta <- theta + epsilon * (phi_t - theta)`。

## 核心要点
1. 一阶近似，省掉二阶项。
2. 资源开销低，工程上常见。
3. 适合做快速适配型元学习基线。

## 这篇论文里怎么用
- [[IBFS]]: 在预备知识中以 Reptile 说明一阶元学习在 FSL 中的可行性。

## 代表工作
- Nichol et al. (2018): Reptile 原始论文。
- [[IBFS]]: 将一阶视角用于其搜索理论动机。

## 相关概念
- [[Model-Agnostic Meta-Learning]]
- [[Few-shot Learning]]
