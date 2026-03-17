---
type: concept
language: zh-CN
source_concept_note: "[[Feature Isotropy]]"
aliases: [特征各向同性, Feature Isotropy]
---

# Feature Isotropy 中文条目

## 一句话直觉

Feature Isotropy（特征各向同性）描述的是：表示空间里的特征是否在各个方向上分布得更均匀，而不是挤在少数几个方向上。

## 它为什么重要

更均匀的特征分布通常意味着更稳健的表示，常与更好的迁移和低标注泛化能力相关。

## 一个小例子

如果样本 embedding 在空间中形成“圆润均匀”的云团，各向同性较高；如果几乎都落在一条细线附近，各向同性较低。

## 更正式的定义

可通过特征矩阵（或协方差矩阵）的特征值谱来衡量各向同性：归一化特征值越均匀，表示越各向同性。

## 数学形式（如有必要）

常见指标是归一化特征值熵：

\[
E = \sum_i -\bar{\lambda}_i \log(\bar{\lambda}_i)
\]

熵越大，谱能量分布越均匀。

## 核心要点

1. 它关注表示几何结构，不等同于最终准确率。
2. 但在很多任务中与泛化能力正相关。
3. 用谱熵衡量成本较低，适合代理搜索场景。

## 这篇论文里怎么用

- [[GEN-TPC-NAS]]: 用每层每头特征谱的熵构造 Entropy score，作为泛化能力代理。

## 代表工作

- [[GEN-TPC-NAS]]: 在 zero-shot NAS 中显式引入各向同性启发的泛化代理。

## 相关概念

- [[Self-Supervised Learning]]
- [[Spearman's Rank Correlation]]

