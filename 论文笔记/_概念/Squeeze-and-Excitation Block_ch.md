---
type: concept
language: zh-CN
source_concept_note: "[[Squeeze-and-Excitation Block]]"
aliases: [SE 模块, SE Block]
---

# Squeeze-and-Excitation Block 中文条目

## 一句话直觉
SE 模块就是“给每个通道打分再加权”，让更有用的通道更突出。

## 它为什么重要
它可以低成本提升特征质量；在鲁棒任务中常带来额外收益。

## 一个小例子
当某些通道对类别判别更稳定时，SE 会提高这些通道的权重，降低噪声通道影响。

## 更正式的定义
先全局池化得到通道统计，再通过两层映射生成通道权重，最后把权重乘回特征图。

## 数学形式（如有必要）

$$
z_c=\frac{1}{HW}\sum_{i=1}^{H}\sum_{j=1}^{W}X_{c,i,j}
$$

再经 `g(z)=\sigma(W_2 \delta(W_1 z))` 生成通道门控向量。

## 核心要点
1. reduction ratio `r` 很关键。
2. `r` 太大时可能过度压缩。
3. 插件化设计便于迁移到不同 backbone。

## 这篇论文里怎么用
- [[Robust Principles]]: 对 `r` 做 sweep，建议 `r=4`，并报告鲁棒精度提升。

## 代表工作
- [[Robust Principles]]: 给出 SE 在对抗鲁棒场景下的系统分析。

## 相关概念
- [[Convolutional Stem]]
- [[Adversarial Robustness]]

