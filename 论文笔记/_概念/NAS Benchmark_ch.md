---
type: concept
language: zh-CN
source_concept_note: "[[NAS Benchmark]]"
aliases: ["NAS 基准", "NAS Benchmark"]
---

# NAS Benchmark 中文条目

## 一句话直觉

NAS Benchmark 就是“提前把大量候选架构的结果算好并存起来”的搜索测试集。

## 它为什么重要

没有 benchmark，很多 NAS 工作根本难以公平比较，因为每次都重新训练候选网络太贵、噪声也太大。

## 一个小例子

在 NASBench-201 里，可以直接查到某些 cell 架构在 CIFAR-100 或 ImageNet16-120 上的结果，而不需要自己重训。

## 更正式的定义

NAS Benchmark 是为标准化评测 NAS 方法而构建的候选架构与其性能/硬件结果数据库。

## 核心要点

1. benchmark 让 NAS 更可复现。
2. benchmark 的搜索空间是否真实，会直接影响结论是否可信。
3. 如果 benchmark 太偏某一类架构，会让 proxy 表现被高估或低估。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 在多个 benchmark 上统一评测 proxy，并批评它们的搜索空间不够贴近真实部署。

## 代表工作

- [[Zero-shot NAS Survey]]: 综述 standard 与 hardware-aware benchmark。
- [[NAS-Bench-201]]: 经典 tabular benchmark。

## 相关概念

- [[Hardware-aware NAS]]
- [[Hardware Performance Model]]

