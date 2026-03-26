---
type: concept
language: zh-CN
source_concept_note: "[[Hebbian Learning]]"
aliases: [Hebb 学习, 同步激活共同增强]
---

# Hebbian Learning 中文条目

## 一句话直觉
神经元“同时激活”越多，它们之间的连接就越容易被加强。

## 它为什么重要
Hebbian 更新只依赖局部信息，不需要完整反向梯度链路，因此常被视为更生物合理的学习机制。

## 一个小例子
若某次前向中输入单元 `x_i` 与输出单元 `y_j` 同时很强，则 `w_ij` 可以按 `x_i * y_j` 方向增加。

## 更正式的定义
Hebbian Learning 是一种基于前后神经元协同活动的局部突触更新规则，典型形式为 `delta w_ij ∝ x_i * y_j`，并常结合归一化约束稳定训练。

## 核心要点
1. 局部更新，生物可解释性强。
2. 直接用于深网时常需加稳定化技巧（归一化、门控等）。
3. 与 NAS 结合时可作为可选学习规则/算子。

## 这篇论文里怎么用
- [[BioNAS]] 将 Hebbian 卷积作为扩展候选，验证了“规则可搜索”框架的可扩展性。

## 代表工作
- BioNAS 引用的 Hebbian 扩展工作（文献 [1], [29]）。
- [[BioNAS]]: 在 NAS 中混合 Hebbian 规则的实证案例。

## 相关概念
- [[Feedback Alignment]]
- [[Predictive Coding]]
- [[Adversarial Robustness]]

