---
type: concept
language: zh-CN
source_concept_note: "[[Spectral Norm]]"
aliases: [谱范数, 最大奇异值]
---

# Spectral Norm 中文条目

## 一句话直觉
谱范数表示线性映射对输入向量“最强放大倍数”。

## 它为什么重要
在梯度传播分析中，谱范数接近 1 往往意味着更稳定，不容易梯度爆炸或消失。

## 一个小例子
若某层 Jacobian 谱范数为 3，说明存在方向上的梯度会被放大约 3 倍。

## 更正式的定义
对矩阵 `A`，谱范数是其最大奇异值，即 `||A||_2 = sigma_max(A)`。

## 数学形式（如有必要）
\[
\|A\|_2 = \max_{\|x\|_2=1}\|Ax\|_2 = \sigma_{\max}(A)
\]

## 核心要点
1. 刻画最坏情况下的放大系数。
2. 是稳定性/Lipschitz 分析核心量。
3. 在深度网络中常通过近似方式计算。

## 这篇论文里怎么用
- [[AZ-NAS]]: 用 Jacobian 相关谱范数近似构造可训练性指标 `sT`。

## 代表工作
- Pennington 等关于 dynamical isometry 的研究。

## 相关概念
- [[Hutchinson Estimator]]
- [[Training-free NAS]]

