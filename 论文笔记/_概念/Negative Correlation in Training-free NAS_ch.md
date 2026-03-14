---
type: concept
language: zh-CN
source_concept_note: "[[Negative Correlation in Training-free NAS]]"
aliases: [负相关, AZP负相关]
---

# Negative Correlation in Training-free NAS 中文条目

## 一句话直觉
负相关就是“proxy 分越高，真实性能反而越差”，排序方向整个反了。

## 它为什么重要
一旦出现负相关，NAS 搜索会被系统性误导，越搜越偏离高质量架构。

## 一个小例子
如果在某个深子空间里，Spearman rho 从正值降到负值，那么按 proxy 选出的 Top 架构很可能不是最优，而是接近最差。

## 更正式的定义
训练自由 NAS 中的负相关，指 proxy 分数与真实性能之间的秩相关系数为负（如 Spearman rho < 0），导致排序一致性被反转。

## 核心要点
1. 常出现在更深、更非线性的结构子空间。
2. 本质是 proxy 设计问题，不一定是搜索器本身问题。
3. 需要从评分路径层面修复（例如 SAM/NIR）。

## 这篇论文里怎么用
- [[NCD]]: 将其作为核心问题提出，并通过 SAM + NIR 在深子空间恢复正相关。

## 代表工作
- [[NCD]]

## 相关概念
- [[Zero-Cost Proxy]]
- [[Stochastic Activation Masking]]
- [[Non-linear Rescaling]]

