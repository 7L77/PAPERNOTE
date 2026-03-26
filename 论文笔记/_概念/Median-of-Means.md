---
type: concept
aliases: [MoM, Median of Means]
---

# Median-of-Means

## Intuition

普通平均值在“少量极端离群值”出现时会被明显拉偏。Median-of-Means（MoM）先把样本分组、各组求均值，再对这些组均值取中位数，用“中位数抗离群”的性质提高估计稳健性。

## Why It Matters

在鲁棒 NAS 或对抗训练中，梯度/边际增益常有重尾噪声。直接平均会不稳定，MoM 能让排序和估计更稳定。

## Tiny Example

假设 12 个样本里有 2 个异常大值。若直接平均会被拉高；MoM 把样本分 4 组后，每组求均值，再取中位数，异常值只影响少数组，整体更稳。

## Definition

给定样本 \(x_1,\dots,x_n\)，划分为 \(G\) 个不相交组 \(B_1,\dots,B_G\)。先算组均值
\[
\mu_g=\frac{1}{|B_g|}\sum_{i\in B_g}x_i
\]
再定义
\[
\mathrm{MoM}(x_1,\dots,x_n)=\mathrm{median}(\mu_1,\dots,\mu_G)
\]

## Math Form (if needed)

MoM 常用于替代普通均值估计，在重尾分布下可获得更好的偏差-方差权衡。

## Key Points

1. 比普通平均值更抗离群值。
2. 适合重尾噪声或含异常样本的估计任务。
3. 需要选择分组数 \(G\)，过大或过小都可能影响稳定性。

## How This Paper Uses It

- [[RDNAS]]: 在 ROSE 中，MoM 用于稳定 Shapley 边际增益估计，减少对抗训练噪声导致的排名波动。

## Representative Papers

- [[RDNAS]]: 将 MoM 与 IQR 结合用于鲁棒 NAS 的操作评分。

## Related Concepts

- [[Interquartile Range]]
- [[Shapley Value]]
