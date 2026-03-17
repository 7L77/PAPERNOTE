---
type: concept
language: zh-CN
source_concept_note: "[[Generative Adversarial Network]]"
aliases: [生成对抗网络, GAN]
---

# Generative Adversarial Network 中文条目

## 一句话直觉
GAN 是“生成器 vs 判别器”的对抗博弈：生成器负责“造假”，判别器负责“验假”。

## 它为什么重要
GAN 不需要显式建模复杂分布就能生成高质量样本，在数据增强、特征合成和生成建模里都很常见。

## 一个小例子
在 ZSL 里，生成器根据类语义和噪声合成 unseen 特征；如果判别器难以区分真假，这些特征就能训练出更好的分类器。

## 更正式的定义
GAN 本质是极小极大优化：
`min_G max_D V(D,G)`。其中 `G` 把噪声（可带条件）映射到样本空间，`D` 判断样本来自真实分布还是生成分布。

## 核心要点
1. G 和 D 强耦合，结构不匹配会导致训练不稳定。
2. 损失函数与正则项（如梯度惩罚）对训练质量影响很大。
3. 条件 GAN 会把语义条件输入 G/D，提高可控性。

## 这篇论文里怎么用
- [[ZeroNAS]]: 联合搜索 G 和 D 的结构，而不是只搜一个模块。

## 代表工作
- [[ZeroNAS]]: 在 ZSL 任务中把 GAN 结构搜索做成可微优化问题。

## 相关概念
- [[WGAN-GP]]
- [[Zero-Shot Learning]]
- [[Differentiable Architecture Search]]

