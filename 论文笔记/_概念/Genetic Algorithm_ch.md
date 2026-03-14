---
type: concept
language: zh-CN
source_concept_note: "[[Genetic Algorithm]]"
aliases: [遗传算法, GA]
---

# Genetic Algorithm 中文条目

## 一句话直觉

遗传算法把候选解当作“种群”，通过选择、交叉、变异反复迭代，逐步找到更优解。

## 它为什么重要

在 NAS 这种离散、不可导搜索问题里，GA 不依赖梯度，通常比暴力搜索更高效。

## 一个小例子

把每层模块选择编码成整数数组，保留高分个体，随机交叉并小概率变异，重复多代。

## 更正式的定义

遗传算法是受生物进化启发的群体随机优化方法，通过适应度驱动进化过程。

## 数学形式（如有必要）

核心迭代可写为：
`population_t -> selection -> crossover/mutation -> population_{t+1}`。

## 核心要点

1. 适合离散或混合搜索空间。
2. 不要求目标函数可导。
3. 编码方式与算子超参对结果影响很大。

## 这篇论文里怎么用

- [[W-PCA]]: 以 W-PCA 分数为适应度，在参数预算约束下搜索轻量语言模型结构。

## 代表工作

- Regularized Evolution for Image Classifier Architecture Search (Real et al., 2019)。

## 相关概念

- [[Neural Architecture Search]]
- [[Training-free NAS]]
