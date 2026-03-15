---
type: concept
language: zh-CN
source_concept_note: "[[Log-normal Distribution]]"
aliases: [对数正态分布, Log-normal Distribution]
---

# Log-normal Distribution 中文条目

## 一句话直觉
如果一个随机变量取对数后服从正态分布，那么它本身就是对数正态分布，且取值一定为正。

## 它为什么重要
当变量代表“乘法累积效应”或必须为正（如尺度、比率、Lipschitz 上界）时，对数正态分布很自然。

## 一个小例子
令 `Z ~ N(mu, sigma^2)`，取 `X = exp(Z)`，则 `X` 服从对数正态；它通常右偏，偶尔会出现很大值。

## 更正式的定义
`X` 若满足 `ln(X) ~ N(mu, sigma^2)`，则 `X ~ LN(mu, sigma^2)`。

## 数学形式（如有必要）
\[
X \sim \mathrm{LN}(\mu,\sigma^2) \iff \ln X \sim \mathcal N(\mu,\sigma^2)
\]

## 核心要点
1. 取值域是正实数。
2. 独立对数正态变量相乘仍是对数正态。
3. 多个对数正态变量求和一般无闭式，常用近似。

## 这篇论文里怎么用
- [[RACL]]: 用对数正态分布对架构参数采样，既保证正值，又便于推导 Lipschitz 上界分布。

## 代表工作
- Fenton-Wilkinson 近似常用于处理对数正态和分布。

## 相关概念
- [[Lipschitz Constant]]
- [[Confidence Learning]]
- [[Differentiable Architecture Search]]
