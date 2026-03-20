---
type: concept
language: zh-CN
source_concept_note: "[[Inception Score]]"
aliases: [IS, Inception 分数]
---

# Inception Score 中文条目

## 一句话直觉

Inception Score 想同时回答两个问题：单张生成图像看起来是否“像某一类东西”，以及整批生成图像是否覆盖了足够多的类别。

## 它为什么重要

它是早期 GAN 论文里非常常见的指标，因为实现简单，而且能同时兼顾“清晰度”与“类别多样性”。

## 一个小例子

如果生成器生成的每张图都很像狗，分类器也都很自信，那单图质量似乎不错；但因为所有图都挤在一个类别里，整体多样性差，IS 也不会太高。

## 更正式的定义

IS 计算的是生成样本条件标签分布 `p(y|x)` 与总体标签分布 `p(y)` 之间的 KL 散度。单张图分类越确定、整体类别覆盖越广，IS 越高。

## 数学形式（如有必要）

$$
\exp\left(\mathbb{E}_{x} \left[ D_{KL}(p(y|x)\|p(y)) \right]\right)
$$

其中 `p(y|x)` 来自预训练 Inception 分类器。数值越高越好。

## 核心要点

1. IS 看重“分类器置信度”和“类别覆盖”。
2. 它不直接比较生成样本和真实样本的距离。
3. 当分类器和数据分布不匹配时，IS 可能会给出误导性结果。

## 这篇论文里怎么用

- [[EAS-GAN]]: 在 CIFAR-10 和 STL-10 上报告 IS，但作者明确认为 [[Frechet Inception Distance]] 更公平、更全面。

## 代表工作

- [[EAS-GAN]]: 把 IS 当作辅助指标，并指出直接用 IS 做 reward 会导致评价偏置。

## 相关概念

- [[Frechet Inception Distance]]
- [[Generative Adversarial Network]]
- [[Mode Collapse]]

