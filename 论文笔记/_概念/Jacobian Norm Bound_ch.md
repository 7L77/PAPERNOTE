---
type: concept
language: zh-CN
source_concept_note: "[[Jacobian Norm Bound]]"
aliases: [雅可比范数界, Jacobian Bound]
---

# Jacobian Norm Bound 中文条目

## 一句话直觉

输入轻微变化会让输出变多少，可以用 Jacobian 来刻画；Jacobian 范数越小，局部越稳定、越抗扰动。

## 它为什么重要

相较于严格认证下界，Jacobian 范数界更易计算、可微，适合放进 NAS 的内循环做高效鲁棒优化。

## 一个小例子

同一输入附近，若模型 A 的 Jacobian 范数显著小于模型 B，那么同样大小的噪声通常会让 A 的输出变化更小。

## 更正式的定义

对网络输出 `f(x)`，一阶近似：
`f(x+delta)-f(x) ≈ J(x)delta`。
再结合范数不等式，可以把输出变化上界到 Jacobian 行向量范数与扰动半径的乘积。

## 数学形式（如有必要）

\[
\frac{1}{K}\sum_{k=1}^{K}|f_k(x+\delta)-f_k(x)|
\le
\frac{1}{K}\sum_{k=1}^{K}\|J_k(x)\|_q \cdot \|\delta\|_p
\]

其中 \(1/p + 1/q = 1\)。Jacobian 范数越小，局部敏感度越低。

## 核心要点

1. 它主要是局部/一阶鲁棒代理，不是严格全局保证。
2. 可微且高效，适合搜索阶段频繁计算。
3. 相比认证下界，通常更快但可能更松。

## 这篇论文里怎么用

- [[DSRNA]]: 用 Jacobian norm bound 构建 DSRNA-Jacobian 的鲁棒性目标，并与 certified-bound 版本形成互补。

## 代表工作

- [[Jacobian Adversarially Regularized Networks for Robustness]]: 用 Jacobian 正则提升对抗鲁棒性。

## 相关概念

- [[Adversarial Robustness]]
- [[Certified Robustness Lower Bound]]
