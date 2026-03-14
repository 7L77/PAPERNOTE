---
type: concept
language: zh-CN
source_concept_note: "[[Stochastic Activation Masking]]"
aliases: [SAM, 随机激活掩码]
---

# Stochastic Activation Masking 中文条目

## 一句话直觉
SAM 在每次 proxy 评估时随机屏蔽一部分激活值，避免“所有激活都参与求和”导致的非线性过度累积。

## 它为什么重要
activation-based proxy 在深层网络里容易出现相关性塌缩甚至负相关，SAM 能以很低代价缓解这个问题。

## 一个小例子
若每层都把全部 ReLU 激活直接求和，深层会更容易饱和；加入 SAM 后只随机保留部分激活，分数区分度更稳定。

## 更正式的定义
在卷积评分中引入 Bernoulli 掩码：
\[
y = \sum(W \odot M \odot X),\quad M(i,j,k)\sim Bernoulli(1-\alpha)
\]
其中 `alpha` 控制掩码强度。

## 核心要点
1. SAM 是评分路径修正，不是重构整个 NAS 算法。
2. 目标是抑制非线性累积引起的分数幅值畸变。
3. 常与 [[Non-linear Rescaling]] 联合使用。

## 这篇论文里怎么用
- [[NCD]]: 将 SAM 作为第一步修正，用于恢复 AZP 的正相关排序能力。

## 代表工作
- [[NCD]]

## 相关概念
- [[Non-linear Rescaling]]
- [[Negative Correlation in Training-free NAS]]
- [[Zero-Cost Proxy]]

