---
type: concept
language: zh-CN
source_concept_note: "[[NAS-Rob-Bench-201]]"
aliases: [鲁棒 NAS-Bench-201, NASRobBench201]
---

# NAS-Rob-Bench-201 中文条目

## 一句话直觉
NAS-Rob-Bench-201 是一个“可查表”的鲁棒 NAS 基准：把大量架构的对抗训练结果预先算好，后续搜索算法可以直接比较。

## 它为什么重要
鲁棒 NAS 最大成本在反复对抗训练。这个基准把高成本离线化，让算法比较更公平、更快、更可复现。

## 一个小例子
你可以在固定 query 预算下比较随机搜索、进化搜索、局部搜索的 PGD 指标，而不必每次从头重训所有候选架构。

## 更正式的定义
NAS-Rob-Bench-201 基于 NAS-Bench-201 搜索空间，报告 6466 个非同构架构在对抗训练后的 clean 与 robust 指标（如 FGSM/PGD/APGD 相关评测）。

## 核心要点
1. 它是固定搜索空间下的鲁棒 tabular benchmark。
2. 适合做预算受控的 robust NAS 对比。
3. 核心价值是“离线重训练一次，在线高效查表多次”。

## 这篇论文里怎么用
- [[NAS-RobBench-201]]：该论文就是这个基准的提出与分析工作。
- [[TRNAS]]：在该基准上进行 robust NAS 方法对比验证。

## 代表工作
- [[NAS-RobBench-201]]：定义并公开该 benchmark。
- [[TRNAS]]：在该 benchmark 上验证鲁棒搜索效率与性能。

## 相关概念
- [[RobustBench]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]

