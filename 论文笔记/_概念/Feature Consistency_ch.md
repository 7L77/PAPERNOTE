---
type: concept
language: zh-CN
source_concept_note: "[[Feature Consistency]]"
aliases: [特征一致性, 扰动下特征一致性]
---

# Feature Consistency 中文条目

## 一句话直觉
鲁棒模型在 clean 样本和扰动样本上应提取到接近的语义特征。

## 为什么重要
如果特征在扰动下变化过大，分类头会更容易输出错误预测。

## 小例子
对同一张图像 `x` 和其 FGSM 扰动 `x'`，若 `cos(e(x), e(x'))` 高，则模型更可能鲁棒。

## 定义
特征一致性是指 clean/perturbed 输入在表示空间中的相似程度，通常按层计算。

## 关键点
1. 它是“表示层面”的鲁棒信号。
2. 可在训练前或极少训练下估计。
3. 应在多种扰动下共同考察。

## 在本文中的作用
- [[CRoZe]] 用 `Z_m` 表示层级特征一致性，并与其他两项相乘构成最终 proxy。

## 代表工作
- [[CRoZe]]

## 相关概念
- [[Parameter Consistency]]
- [[Gradient Alignment]]
- [[Adversarial Robustness]]
