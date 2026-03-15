---
type: concept
language: zh-CN
source_concept_note: "[[Parameter Consistency]]"
aliases: [参数一致性, 更新参数一致性]
---

# Parameter Consistency 中文条目

## 一句话直觉
如果 clean 与 perturbed 目标对参数更新方向更一致，模型更容易同时兼顾两者。

## 为什么重要
更新方向冲突越小，训练轨迹越稳定，最终鲁棒性通常更好。

## 小例子
分别对 clean loss 和 perturbed loss 做一步更新，若 `theta_1` 与 `theta_1^r` 相似度高，说明参数一致性好。

## 定义
参数一致性是指在 clean/perturbed 目标下得到的参数状态（或更新方向）之间的相似程度。

## 关键点
1. 本质是“优化兼容性”信号。
2. 单步估计计算成本低。
3. 与特征一致性互补。

## 在本文中的作用
- [[CRoZe]] 用 `P_m` 量化层级参数一致性（Eq. 8），并参与最终 proxy 聚合。

## 代表工作
- [[CRoZe]]

## 相关概念
- [[Feature Consistency]]
- [[Gradient Alignment]]
- [[Robust Neural Architecture Search]]
