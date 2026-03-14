---
type: concept
language: zh-CN
source_concept_note: "[[Training-free NAS]]"
aliases: [免训练NAS, Training-free NAS]
---

# Training-free NAS 中文条目

## 一句话直觉
Training-free NAS 指在搜索阶段不完整训练每个候选网络，而用代理信号快速估计架构优劣。

## 它为什么重要
它能把架构搜索成本大幅降低，使大规模候选评估变得可行。

## 一个小例子
原本要训练几千个候选网络，现在先用 proxy 打分，只训练极少数高分架构。

## 更正式的定义
Training-free NAS 是在搜索阶段避免迭代式完整训练，依赖训练前或极低成本指标进行候选架构排序的 NAS 范式。

## 数学形式（如有必要）
常见形式是在预算约束下最大化 proxy 排序质量或与真实精度的一致性。

## 核心要点
1. 关键在“快筛选”，不是直接替代最终训练。
2. 搜索效果高度依赖 proxy 与真实性能的相关性。
3. 常与进化搜索、随机搜索结合。

## 这篇论文里怎么用
- [[AZ-NAS]]: 在训练自由框架下组合四类 proxy，并用非线性聚合提高排序一致性。

## 代表工作
- TE-NAS (ICLR 2021).
- AZ-NAS (CVPR 2024).

## 相关概念
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]

