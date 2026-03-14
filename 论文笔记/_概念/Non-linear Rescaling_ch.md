---
type: concept
language: zh-CN
source_concept_note: "[[Non-linear Rescaling]]"
aliases: [NIR, 非线性重标定]
---

# Non-linear Rescaling 中文条目

## 一句话直觉
NIR 的目标是把 proxy 分数从“非线性过饱和”状态拉回可比较区间，让排序重新可信。

## 它为什么重要
如果激活求和导致分数尺度失真，架构越深分数反而越低，最终会出现与真实性能负相关的问题。

## 一个小例子
深层架构在原始 AZP 下可能都挤在低分区；加入 NIR 后分数拉开，高质量架构重新回到前列。

## 更正式的定义
NIR 在 [[NCD]] 中基于 BN/LN 求和机制分析提出：通过在 AZP 评估时采用更稳定的归一化/重标定路径（LN 视角），降低非线性放大效应。

## 核心要点
1. NIR 调的是评分尺度，不是直接改搜索空间。
2. 与 [[Stochastic Activation Masking]] 互补，二者联合效果最好。
3. 深子空间下收益更明显。

## 这篇论文里怎么用
- [[NCD]]: 与 SAM 联合，把 77-conv 子空间中的负相关恢复为正相关。

## 代表工作
- [[NCD]]

## 相关概念
- [[Stochastic Activation Masking]]
- [[Negative Correlation in Training-free NAS]]
- [[Zero-Cost Proxy]]

