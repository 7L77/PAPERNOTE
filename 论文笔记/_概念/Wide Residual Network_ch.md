---
type: concept
language: zh-CN
source_concept_note: "[[Wide Residual Network]]"
aliases: [宽残差网络, WRN, Wide ResNet]
---

# Wide Residual Network 中文条目

## 一句话直觉
Wide Residual Network（WRN）不是一味加深网络，而是通过“加宽通道”提升残差网络能力。

## 它为什么重要
WRN 是对抗训练里非常常见的骨干；很多鲁棒架构研究本质上都在比较 WRN 的深度-宽度组合。

## 一个小例子
`WRN-34-10` 通常表示深度 34、宽度倍率 10 的残差网络，相比普通 ResNet 通道更宽。

## 更正式的定义
WRN 属于 ResNet 家族，通过宽度因子 `k` 放大通道数，形成“较少层数但更宽”的残差块结构，通常记作 `WRN-depth-width`。

## 数学形式（如有必要）
若某 stage 的基准通道为 `n_i`，WRN 可写作 `k * n_i`，其中 `k` 为宽度系数。

## 核心要点
1. 加宽常带来更强表示能力与更稳定优化行为。
2. WRN 提供了研究深度-宽度权衡的自然坐标系。
3. 在鲁棒学习中，WRN 是高频基线架构族。

## 这篇论文里怎么用
- [[NARes]]: 将 WRN 宏观设计作为完整搜索空间，系统枚举 stage 级深宽组合。

## 代表工作
- Zagoruyko and Komodakis (2017): WRN 原始论文。
- [[NARes]]: 在 WRN 宏观空间上构建大规模鲁棒性数据集。

## 相关概念
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]

