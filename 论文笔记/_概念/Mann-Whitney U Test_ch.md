---
type: concept
language: zh-CN
source_concept_note: "[[Mann-Whitney U Test]]"
aliases: [曼-惠特尼U检验, Wilcoxon秩和检验]
---

# Mann-Whitney U Test 中文条目

## 一句话直觉
[[Mann-Whitney U Test]] 用“排序”而不是“正态分布假设”来判断两组样本谁更大。

## 它为什么重要
在 NAS 的多次 proxy 打分场景中，样本少且分布常偏态；U 检验比只比均值更稳健。

## 一个小例子
架构 A、B 各有 10 次打分。若 A 的分数在总体排序里大多排在 B 之前，U 检验会给出 A 更优的统计证据。

## 更正式的定义
给定两组独立样本 `X` 和 `Y`，先做合并排序，再由秩和计算 U 统计量。

- `H0`: 两组来自相同分布。
- `H1`（单侧）: `X` 在分布上倾向于大于 `Y`。

## 数学形式（如有必要）
常见写法之一：

\[
U_X = R_X - \frac{n_X(n_X+1)}{2}
\]

其中 `R_X` 是 `X` 在合并样本中的秩和。p 值越小，越支持拒绝 `H0`。

## 核心要点
1. 非参数检验，不强依赖正态假设。
2. 适合 noisy、小样本比较。
3. 单侧检验适合“谁更好”这类方向性决策。

## 这篇论文里怎么用
- [[Variation-Matters]]：Sec. 4.2 / Algorithm 1 中把 U 检验作为架构比较器，替代均值比较。

## 代表工作
- [[Variation-Matters]]：在 random/evolutionary search 决策环节直接使用 U-test。

## 相关概念
- [[Stochastic Dominance]]
- [[Coefficient of Variation]]
- [[Evolutionary Neural Architecture Search]]

