---
type: concept
language: zh-CN
source_concept_note: "[[Frechet Inception Distance]]"
aliases: [FID, Fréchet Inception Distance, 弗雷歇 Inception 距离]
---

# Frechet Inception Distance 中文条目

## 一句话直觉

Frechet Inception Distance，简称 FID，可以理解成“生成样本整体分布和真实样本整体分布有多像”。它不是只看一张图好不好看，而是看整批生成图在特征空间里离真实图有多远。

## 它为什么重要

GAN 很容易出现“少数样本很好看，但整体分布不对”的情况。FID 同时惩罚样本不真实和模式覆盖不全，所以比只看局部质量更有用。

## 一个小例子

如果真实数据里有猫、狗、车，但生成器只会生成猫，而且猫看起来还挺真，那么单看几张图可能觉得不错；可一旦看整体分布，生成样本覆盖太窄，FID 还是会偏高。

## 更正式的定义

FID 在 Inception 网络提取的特征空间里，把真实样本和生成样本分别近似成高斯分布，然后计算这两个高斯分布之间的 Fréchet distance。

## 数学形式（如有必要）

设真实特征的均值和协方差为 `(μ_r, Σ_r)`，生成特征的均值和协方差为 `(μ_g, Σ_g)`，则

$$
\mathrm{FID} =
\|\mu_r - \mu_g\|_2^2 +
\mathrm{Tr}(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2})
$$

其中：
- `μ` 衡量分布中心差异
- `Σ` 衡量分布形状和扩散程度差异
- 数值越小越好

## 核心要点

1. FID 看的是“分布距离”，不是单张图像打分。
2. FID 越低，说明生成分布越接近真实分布。
3. 当我们关心 diversity 和 mode coverage 时，FID 通常比 [[Inception Score]] 更稳健。

## 这篇论文里怎么用

- [[EAS-GAN]]: 把 FID 当成主要定量指标，用来证明搜索后的 generator architecture 比 E-GAN、AGAN、WGAN-GP 等基线更好。

## 代表工作

- [[EAS-GAN]]: 展示了架构搜索可以直接带来更低的 FID。

## 相关概念

- [[Inception Score]]
- [[Generative Adversarial Network]]
- [[Mode Collapse]]

