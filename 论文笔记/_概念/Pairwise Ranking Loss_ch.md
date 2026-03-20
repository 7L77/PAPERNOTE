---
type: concept
language: zh-CN
source_concept_note: "[[Pairwise Ranking Loss]]"
aliases: [Pairwise Loss, Pairwise Ranking Objective]
---

# Pairwise Ranking Loss 中文条目

## 一句话直觉

Pairwise Ranking Loss 通过“样本两两比较”学习排序：该在前面的样本被排后面就惩罚。

## 它为什么重要

低样本 NAS 中，预测绝对精度很难，但学“谁比谁更好”往往更容易，也更实用。

## 一个小例子

真实上 A>B，但预测给出 \(\hat{y}_A < \hat{y}_B\)，则该对样本触发损失惩罚。

## 更正式的定义

一般形式：
\[
\mathcal{L}_{pair}=\frac{1}{|\mathcal{N}|}\sum_{(i,j)\in\mathcal{N}} \ell\!\left(s_{ij}(\hat{y}_i-\hat{y}_j)\right)
\]
其中 \(s_{ij}\) 表示真实顺序符号，\(\ell\) 可取 hinge/logistic 等。

## 数学形式（如有必要）

- HR: \(\ell(z)=\max(0,m-z)\)
- LR: \(\ell(z)=\log(1+\exp(-z))\)
- 核心是减少错序 pair 数量或错序强度。

## 核心要点

1. 更偏向相对排序学习。
2. 在极低样本阶段常比 weighted loss 更稳。
3. 不能直接保证整张列表全局最优一致。

## 这篇论文里怎么用

- [[PWLNAS]]: 比较 HR/LR/MSE+SR 等 pairwise 变体，并将 HR 用于多项分段策略前期。

## 代表工作

- [[PWLNAS]]: 给出 pairwise 在不同预算下的优势与边界。

## 相关概念

- [[Listwise Ranking Loss]]
- [[Kendall's Tau]]
