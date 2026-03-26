---
type: concept
language: zh-CN
source_concept_note: "[[Predictive Coding]]"
aliases: [预测编码, 预测误差最小化]
---

# Predictive Coding 中文条目

## 一句话直觉
每一层都在“预测”相邻层活动，并通过最小化预测误差来学习。

## 它为什么重要
预测编码提供了不同于 BP 的学习图景：把学习看成局部误差修正过程，更贴近部分神经科学假设。

## 一个小例子
上层给出预测信号，下层真实激活与预测不一致时形成误差；网络通过反复迭代减少该误差。

## 更正式的定义
Predictive Coding 是一种分层误差最小化框架：各层持续比较“预测值与观测值”，并通过局部更新迭代地降低预测误差。

## 核心要点
1. 以“误差驱动推断”替代严格反向梯度传播。
2. 通常需要多步迭代，计算开销可能上升。
3. 实现中常加入归一化、阻尼或门控保障稳定性。

## 这篇论文里怎么用
- [[BioNAS]] 将 Predictive Coding 卷积作为可选候选，验证混合规则搜索框架可容纳更广泛的生物启发机制。

## 代表工作
- BioNAS 背景部分讨论了预测编码及相关前向学习范式。
- [[BioNAS]]: 预测编码进入 NAS 搜索空间的应用示例。

## 相关概念
- [[Feedback Alignment]]
- [[Hebbian Learning]]
- [[Neural Architecture Search]]

