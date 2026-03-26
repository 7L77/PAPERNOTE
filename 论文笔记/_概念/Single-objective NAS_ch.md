---
type: concept
language: zh-CN
source_concept_note: "[[Single-objective NAS]]"
aliases: [单目标NAS, SONAS]
---

# Single-objective NAS 中文条目

## 一句话直觉
单目标 NAS（SONAS）只优化一个分数，最后输出一个“最优架构”。

## 它为什么重要
它实现简单，但容易忽略精度、鲁棒性、成本等目标之间的权衡。

## 一个小例子
如果只最大化 `Val-Acc-12`，可能会选到早期验证精度高但对抗鲁棒性一般的架构。

## 更正式的定义
\[
\min_{x \in \mathcal{A}} f(x)
\]
其中 \(f\) 是单一目标函数，\(x\) 是搜索空间中的架构。

## 核心要点
1. 单目标、单最优解。
2. 设置更简单，调参成本较低。
3. 容易错过多目标权衡下的优质解。

## 这篇论文里怎么用
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 用 GA 构建单目标变体（Val-Acc-12 与 SynFlow）做对比。

## 代表工作
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 发现对抗训练评测下，训练式目标的 SONAS 通常优于 SynFlow-SONAS。

## 相关概念
- [[Multi-objective NAS]]
- [[Genetic Algorithm]]

