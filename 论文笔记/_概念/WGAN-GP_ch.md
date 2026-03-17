---
type: concept
language: zh-CN
source_concept_note: "[[WGAN-GP]]"
aliases: [带梯度惩罚的Wasserstein GAN, WGAN-GP]
---

# WGAN-GP 中文条目

## 一句话直觉
WGAN-GP 用 Wasserstein 风格目标替代普通 GAN 判别损失，并通过梯度惩罚约束判别器的光滑性，从而让训练更稳。

## 它为什么重要
普通 GAN 训练容易震荡或崩溃，WGAN-GP 通常能提供更稳定的梯度和更可靠的优化过程。

## 一个小例子
当判别器过于“尖锐”时，生成器拿到的梯度会失真。WGAN-GP 在 real/fake 插值样本上约束梯度范数接近 1，可显著缓解这种问题。

## 更正式的定义
WGAN-GP 的典型目标可写为：
`E[D(fake)] - E[D(real)] + lambda * E[(||∇_x_hat D(x_hat)||_2 - 1)^2]`，
其中 `x_hat` 是 real 与 fake 的插值点。

## 核心要点
1. 判别器输出通常不经 sigmoid，直接作为 critic 分数。
2. 梯度惩罚在插值样本上计算。
3. 常配合“多次更新 D，再更新一次 G”的训练节奏。

## 这篇论文里怎么用
- [[ZeroNAS]]: 在搜索阶段与重训练阶段都使用 WGAN-GP 项，并与分类损失联合优化。

## 代表工作
- [[ZeroNAS]]: 在可微 GAN 架构搜索中系统使用 WGAN-GP。

## 相关概念
- [[Generative Adversarial Network]]
- [[Differentiable Architecture Search]]
- [[Zero-Shot Learning]]

