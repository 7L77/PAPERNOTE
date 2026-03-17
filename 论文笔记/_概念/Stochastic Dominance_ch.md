---
type: concept
language: zh-CN
source_concept_note: "[[Stochastic Dominance]]"
aliases: [随机占优, 一阶随机占优]
---

# Stochastic Dominance 中文条目

## 一句话直觉
[[Stochastic Dominance]] 是“看整条分布谁更好”，而不是只比平均数。

## 它为什么重要
两个方法均值可能接近，但一个方法尾部风险更大。随机占优可以把这种风险差异显式纳入比较。

## 一个小例子
方法 A 与 B 均值一样，但 A 很少出现极差结果，B 经常出现极差结果。即使均值相同，A 也可能在分布意义上更优。

## 更正式的定义
若随机变量 `X` 相对 `Y` 一阶随机占优，则：

\[
P(X>k)\ge P(Y>k),\ \forall k
\]

并且至少存在一个阈值 `k` 满足严格大于。

等价地可写成 CDF 形式：

\[
F_X(k)\le F_Y(k),\ \forall k
\]

且某处严格小于。

## 数学形式（如有必要）
- `k` 是性能阈值。
- 随机占优通常蕴含更高期望，但“期望更高”不必然推出随机占优。

## 核心要点
1. 随机占优比均值比较更严格。
2. 能体现尾部风险与稳定性。
3. 在 noisy ranking 下更适合作为“谁更好”的判据。

## 这篇论文里怎么用
- [[Variation-Matters]]：Sec. 4.2 用 Mann-Whitney 检验来近似判断架构分布优劣。

## 代表工作
- [[Variation-Matters]]：以随机占优思想替代平均值排序。

## 相关概念
- [[Mann-Whitney U Test]]
- [[Coefficient of Variation]]
- [[Kendall's Tau]]

