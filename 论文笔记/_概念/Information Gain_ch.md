---
type: concept
language: zh-CN
source_concept_note: "[[Information Gain]]"
aliases: [信息增益, IG]
---

# Information Gain 中文条目

## 一句话直觉
Information Gain（信息增益）表示：在已经知道一部分信息后，再知道一个新变量，能把目标不确定性再减少多少。

## 它为什么重要
在 NAS 的多 proxy 组合里，我们不只关心“单个 proxy 准不准”，还关心“新 proxy 是否提供了额外信息”，避免重复堆叠同类信号。

## 一个小例子
如果 `z1` 已经能把架构好坏排得很清楚，而加入 `z2` 后对验证精度的不确定性几乎没变，那么 `IG(z2)` 就很小，说明 `z2` 对 `z1` 基本是冗余信息。

## 更正式的定义
给定目标变量 `y` 和两个 proxy 变量 `z_i, z_j`，常见条件信息增益写作：
\[
IG(z_j)=H(y|z_i)-H(y|z_i,z_j)
\]
其中 `H(.)` 是熵。值越大，表示 `z_j` 在 `z_i` 已知的前提下提供的新增信息越多。

## 核心要点
1. IG 是“有条件”的量，取决于已知变量集合。
2. IG 低通常表示冗余，IG 高通常表示互补。
3. 实际估计会受样本量和熵估计方式影响。

## 这篇论文里怎么用
- [[L-SWAG]]: 在 LIBRA 中，作者在高相关候选里用最小 IG 选择第二个 proxy（Sec. 3.2, Eq. 9），作为经验型组合策略的一部分。

## 代表工作
- [[ZCP-Eval]]: 用多 proxy 统计与排序分析来比较 proxy 行为。
- [[L-SWAG]]: 把 IG 放进可执行的 proxy 选择算法（LIBRA）中。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Proxy Voting]]
