---
type: concept
language: zh-CN
source_concept_note: "[[Precision@T]]"
aliases: [Top-T 精确率, Precision at T]
---

# Precision@T 中文条目

## 一句话直觉

Precision@T 看的是“你挑出来的前 T 个候选里，有多少个真的属于真实性能前 T”。

## 它为什么重要

在 NAS 里我们通常只会重点训练少量候选，所以“前排候选够不够准”比“全局排序是否完美”更关键。

## 一个小例子

若 T=5，代理指标选出的前 5 个架构中有 3 个也在真实性能前 5，那么 Precision@5=3/5=0.6。

## 更正式的定义

设代理排序为 \(R_M\)，真实排序为 \(R_f\)，则：

\[
\rho_T(M,f)=\frac{|\{A \mid R_M(A)\le T \land R_f(A)\le T\}|}{T}
\]

它衡量的是两个 top-T 集合的重叠比例。

## 数学形式（如有必要）

- \(A\): 候选架构。
- \(R_M(A)\): 在代理指标下的排名。
- \(R_f(A)\): 在真实性能下的排名。
- \(T\): 截断阈值（top-k）。

## 核心要点

1. 关注的是“候选池前排质量”，不是全局排序一致性。
2. 与预算受限搜索高度一致。
3. 两个方法即便 Kendall/Spearman 接近，Precision@T 也可能差很多。

## 这篇论文里怎么用
- [[RoBoT]]: 用 Precision@T 定量“估计缺口”，并支撑后续贪心利用阶段。

## 代表工作

- [[RoBoT]]: 将 Precision@T 放入训练免费 NAS 的理论与算法分析。

## 相关概念

- [[Training-free NAS]]
- [[Kendall's Tau]]
