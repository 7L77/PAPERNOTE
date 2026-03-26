---
type: concept
aliases: [IQR, Quartile Range]
---

# Interquartile Range

## Intuition

Interquartile Range（IQR）衡量“中间 50% 数据”的离散程度：只看第 25 百分位到第 75 百分位之间的跨度，天然弱化极端值影响。

## Why It Matters

当数据有离群值时，方差和均值会被异常点放大。IQR 更稳健，常用于异常检测与鲁棒统计。

## Tiny Example

数据 `[1,2,2,3,3,4,100]` 中，100 是离群值。IQR 主要由中间数据决定，不会像均值/方差那样被 100 大幅拉动。

## Definition

记第一四分位数为 \(Q_1\)，第三四分位数为 \(Q_3\)，则
\[
\mathrm{IQR}=Q_3-Q_1
\]

常见异常阈值：
\[
x<Q_1-1.5\mathrm{IQR}\quad \text{or}\quad x>Q_3+1.5\mathrm{IQR}
\]

## Math Form (if needed)

IQR 本质是分位数统计，适合重尾或非高斯噪声环境。

## Key Points

1. 对极端值不敏感。
2. 适合做异常值筛查。
3. 常与稳健估计器（如 MoM）搭配使用。

## How This Paper Uses It

- [[RDNAS]]: 在 ROSE 中，IQR 用来标记 Shapley 边际增益的异常波动，避免“关键但稀有”的操作贡献被平均抹掉。

## Representative Papers

- [[RDNAS]]: 将 IQR 与 MoM 结合用于对抗 NAS 中的鲁棒操作评分。

## Related Concepts

- [[Median-of-Means]]
- [[Shapley Value]]
