---
type: concept
language: zh-CN
source_concept_note: "[[NAS-RobBench-201]]"
aliases: [鲁棒NAS-Bench-201, NAS-RobBench-201]
---

# NAS-RobBench-201 中文条目

## 一句话直觉
NAS-RobBench-201 是一个“对抗训练后再评测”的鲁棒 NAS 基准表。

## 它为什么重要
它让我们可以低成本比较不同 NAS 策略在 clean 与多攻击鲁棒性上的表现，而不必每次重复重训。

## 一个小例子
给定一个架构 ID，就能直接查到该架构在 clean、FGSM、PGD、AutoAttack 下的精度。

## 更正式的定义
NAS-RobBench-201 在 NAS-Bench-201 风格的表格基准上扩展了对抗训练与多攻击鲁棒评测指标。

## 核心要点
1. 关注“对抗训练后”的鲁棒表现。
2. 适合做可复现、低成本的算法比较。
3. 与非 AT 鲁棒数据集相比，可能得到不同方法排序。

## 这篇论文里怎么用
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 用它评估 GA/NSGA-II 搜索结果的 clean/robust 指标。

## 代表工作
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 在该基准上比较 training-based 与 training-free 目标。

## 相关概念
- [[NAS-Bench-201]]
- [[Adversarial Training]]

