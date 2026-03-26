---
type: concept
language: zh-CN
source_concept_note: "[[Feedback Alignment]]"
aliases: [FA, 随机反馈对齐]
---

# Feedback Alignment 中文条目

## 一句话直觉
FA 的核心是不用严格反向转置权重传梯度，而是用固定随机反馈也能驱动网络学习。

## 它为什么重要
BP 需要前后向权重精确对称，这在生物神经系统上不太合理；FA 提供了更“生物启发”的信用分配路径。

## 一个小例子
两层网络里，BP 用 `W2^T` 回传误差；FA 用固定随机矩阵 `B2` 回传，隐藏层仍可更新。

## 更正式的定义
Feedback Alignment 是一种信用分配机制：隐藏层更新依赖固定随机反馈矩阵，而不是严格的反向转置梯度链路。

## 核心要点
1. 生物可解释性高于标准 BP。
2. 精度通常不及 BP，但能在部分任务上接近可用。
3. uSF/brSF/frSF 可视为在符号与幅值上对 FA 的进一步结构化约束。

## 这篇论文里怎么用
- [[BioNAS]] 把 FA 作为可搜索学习规则之一，并允许在不同层与其他规则混合。

## 代表工作
- [[Feedback Alignment]]: 经典随机反馈对齐路线。
- [[Benchmarking the accuracy and robustness of biologically inspired neural networks]]: 生物启发规则的准确率与鲁棒性评测背景。

## 相关概念
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Hebbian Learning]]
- [[Predictive Coding]]

