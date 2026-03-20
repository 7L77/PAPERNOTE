---
type: concept
language: zh-CN
source_concept_note: "[[Mode Collapse]]"
aliases: [模式崩塌, GAN 模式崩塌]
---

# Mode Collapse 中文条目

## 一句话直觉

Mode Collapse 指的是：生成器明明应该覆盖很多种真实样本模式，但最后只会反复生成少数几种结果。

## 它为什么重要

这是 GAN 最经典的失败现象之一。模型可能生成出来的图单看还不错，但整体上“花样太少”，说明它根本没学到真实分布的多样性。

## 一个小例子

如果真实数据里有很多卧室布局，但生成器来回只会生成两三种床和墙面组合，那么它虽然能骗过一些局部判断，却已经发生了模式崩塌。

## 更正式的定义

Mode Collapse 是生成模型，尤其是 GAN，在学习目标分布时只覆盖少数模式、忽略其余模式的现象。它通常和对抗训练不稳定、梯度信号不足或结构设计不合理有关。

## 核心要点

1. 生成样本“好看”不代表没有 mode collapse。
2. 模式崩塌本质上是分布覆盖不足，而不只是清晰度问题。
3. loss、判别器行为和网络结构都会影响崩塌风险。

## 这篇论文里怎么用

- [[EAS-GAN]]: 用多种 mutation objective 和 diversity-aware fitness 来抑制训练中的模式崩塌风险。

## 代表工作

- [[EAS-GAN]]: 把 mutation diversity 和 evolutionary selection 当作缓解模式崩塌的关键机制。

## 相关概念

- [[Generative Adversarial Network]]
- [[Frechet Inception Distance]]
- [[Inception Score]]

