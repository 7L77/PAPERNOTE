---
type: concept
language: zh-CN
source_concept_note: "[[Denoising Block]]"
aliases: [去噪模块, Feature Denoising Block]
---

# Denoising Block 中文条目

## 一句话直觉
Denoising block 在特征空间做平滑/聚合，削弱对抗噪声带来的异常激活。

## 它为什么重要
对抗扰动往往污染中间特征；在特征层做去噪有助于提升鲁棒性。

## 一个小例子
非局部去噪会按相似度对全局位置特征加权平均，使局部异常值被“稀释”。

## 更正式的定义
去噪块通常由去噪算子（如 non-local mean）和投影/残差连接组成，用于产生更稳定的特征表示。

## 数学形式（如有必要）
\[
z_p=\frac{1}{C(x)}\sum_{q\in L} f(x_p,x_q)x_q
\]
其中 `f` 是相似度权重函数，`C(x)` 是归一化项。

## 核心要点
1. 主要作用在中间特征而非输入像素。
2. 可能提升鲁棒性，但会增加计算量。
3. 插入位置（前层/中层）会影响效果。

## 这篇论文里怎么用
- [[ABanditNAS]]: 将 denoising block 纳入 NAS 候选操作，用于搜索更鲁棒结构。

## 代表工作
- Buades et al. (2005): non-local means。
- Xie et al. (CVPR 2019): feature denoising for adversarial robustness。

## 相关概念
- [[Gabor Filter]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]

