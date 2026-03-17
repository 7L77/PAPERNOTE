---
type: concept
language: zh-CN
source_concept_note: "[[Bayesian Neural Network]]"
aliases: [贝叶斯神经网络, Bayesian Neural Network]
---

# Bayesian Neural Network 中文条目

## 一句话直觉
贝叶斯神经网络把“参数值”看成“参数分布”，因此不仅有预测值，还有不确定性。

## 它为什么重要
在小样本或高噪声场景，不确定性估计有助于提升排序与决策稳定性。

## 一个小例子
普通网络给出单点权重 `w=0.8`；BNN 学到一个围绕 0.8 的分布，并在预测时反映置信区间。

## 更正式的定义
BNN 对权重后验分布建模，并在推理时对权重分布积分或采样近似。

## 数学形式（如有必要）
\[
W = \mu + \sigma \odot \epsilon,\quad \epsilon \sim \mathcal{N}(0,I)
\]

## 核心要点
1. 显式建模认知不确定性。
2. 更适合低数据预算任务。
3. 训练和推理通常比确定性网络更重。

## 这篇论文里怎么用
- [[ParZC]]: 在 mixer 前后加入 Bayesian 层，提升节点统计不确定性建模能力。

## 代表工作
- [[ParZC]]: 将 BNN 融入 ZC 排序器。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
- [[Kendall's Tau]]
