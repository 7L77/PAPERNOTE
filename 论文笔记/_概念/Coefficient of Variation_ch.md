---
type: concept
language: zh-CN
source_concept_note: "[[Coefficient of Variation]]"
aliases: [变异系数, CV]
---

# Coefficient of Variation 中文条目

## 一句话直觉
[[Coefficient of Variation]]（CV）衡量的是“波动相对均值有多大”，不是只看绝对波动。

## 它为什么重要
不同指标量纲和数值范围可能差很多，直接比方差不公平；CV 做了归一化，更适合跨指标/跨搜索空间比较稳定性。

## 一个小例子
两个方法都波动 `±5`：一个均值是 `100`，一个均值是 `10`。后者相对更不稳定，CV 会明显更大。

## 更正式的定义
当均值不为 0 时：

\[
\mathrm{CV}(X)=\frac{\mathrm{Std}(X)}{\mathrm{Mean}(X)}
\]

有些论文会用 `Var/Mean` 作为相对波动指标，阅读时需确认具体定义。

## 数学形式（如有必要）
- `Std(X)`：标准差。
- `Mean(X)`：均值。
- CV 越大，说明相对波动越大。

## 核心要点
1. CV 是“相对波动”，适合不同量级之间比较。
2. 当均值接近 0 或“零点不具物理意义”时，CV 可能不稳健。
3. 在 zero-shot NAS 中，CV 可用于评估 ranking function 的鲁棒性。

## 这篇论文里怎么用
- [[Variation-Matters]]：在 Sec. 4.1 / Eq. (1) 用 CV 聚合定义 ranking variation。

## 代表工作
- [[Variation-Matters]]：把 CV 作为分析 ranking 随机性的核心统计量。

## 相关概念
- [[Stochastic Dominance]]
- [[Mann-Whitney U Test]]
- [[Zero-Cost Proxy]]

