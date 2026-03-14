---
type: concept
language: zh-CN
source_concept_note: "[[NAS-Bench-201]]"
aliases: [NAS-Bench-201基准, NB201]
---

# NAS-Bench-201 中文条目

## 一句话直觉
NAS-Bench-201 是一个“候选架构都提前评好分”的小型 NAS 基准库。

## 它为什么重要
它让研究者不用每次都重训大量网络，就能快速、公平地比较搜索或预测方法。

## 一个小例子
想比较两种 NAS 策略时，可直接在 NAS-Bench-201 上查询性能而不是重复训练 6000+ 架构。

## 更正式的定义
NAS-Bench-201 是 cell-based 的离散搜索空间基准，包含 15,625 个编码（其中 6,466 个 unique/non-isomorphic 架构）及其在 CIFAR-10/100、ImageNet16-120 上的评估结果。

## 核心要点
1. 复现友好，比较更公平。
2. 很适合做代理特征与性能预测研究。
3. 对更大开放搜索空间的外推能力需要额外验证。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 在 NAS-Bench-201 上评估 ZCP 对鲁棒性预测的迁移能力。

## 代表工作
- [[NAS-Bench-201]]: 原始基准工作。
- [[ZCP-Eval]]: 基于该基准做鲁棒代理评估。

## 相关概念
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Robust Neural Architecture Search]]


## 补充（2026-03-14）
- [[AZ-NAS]]: 该论文把 NAS-Bench-201 作为主基准报告排序相关性与选中架构性能。
