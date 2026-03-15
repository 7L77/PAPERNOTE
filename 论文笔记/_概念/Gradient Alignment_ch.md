---
type: concept
language: zh-CN
source_concept_note: "[[Gradient Alignment]]"
aliases: [梯度对齐, 梯度一致性]
---

# Gradient Alignment 中文条目

## 一句话直觉
当 clean 与 perturbed 梯度方向更一致时，模型更容易同时优化两种目标。

## 为什么重要
梯度冲突大时，模型会在不同目标间“拉扯”，容易出现鲁棒性与精度的失衡。

## 小例子
计算 `|cos(g, g^r)|`；值越高表示 clean 与 robust 更新方向越一致。

## 定义
梯度对齐是对不同任务/数据条件下梯度方向一致程度的量化。

## 关键点
1. 它直接反映优化动态。
2. 常用绝对余弦相似度度量。
3. 对齐高通常对应更稳定的联合优化。

## 在本文中的作用
- [[CRoZe]] 定义 `G_m` 为层级梯度对齐项（Eq. 9），并纳入最终 proxy。

## 代表工作
- [[CRoZe]]

## 相关概念
- [[Feature Consistency]]
- [[Parameter Consistency]]
- [[Adversarial Robustness]]
