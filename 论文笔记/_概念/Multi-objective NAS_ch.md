---
type: concept
language: zh-CN
source_concept_note: "[[Multi-objective NAS]]"
aliases: [多目标NAS, MONAS]
---

# Multi-objective NAS 中文条目

## 一句话直觉
多目标 NAS（MONAS）同时优化多个目标，输出的是一组折中解而不是单一最优解。

## 它为什么重要
实际应用通常要同时考虑精度、鲁棒性和效率，MONAS 能把这些冲突目标显式呈现出来。

## 一个小例子
A 架构鲁棒性最高，B 架构速度最快；MONAS 会同时保留它们作为 Pareto 候选。

## 更正式的定义
\[
\min_{x \in \mathcal{A}} [f_1(x), f_2(x), ..., f_k(x)]
\]
并返回非支配解集合。

## 核心要点
1. 输出 Pareto 解集，不是单点最优。
2. 更适合分析 accuracy-robustness-efficiency 权衡。
3. 需要额外规则从解集中选最终部署模型。

## 这篇论文里怎么用
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 使用 NSGA-II 做 MONAS，并用综合排名选代表解。

## 代表工作
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 结果显示 `NSGA-II (SynFlow)` 在所有报告指标上优于 `NSGA-II (Val-Acc-12)`。

## 相关概念
- [[NSGA-II]]
- [[Pareto Front]]

