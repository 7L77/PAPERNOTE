---
type: concept
language: zh-CN
source_concept_note: "[[Hutchinson Estimator]]"
aliases: [Hutchinson估计器, 随机迹估计]
---

# Hutchinson Estimator 中文条目

## 一句话直觉
Hutchinson Estimator 用随机向量近似昂贵矩阵量，从而避免显式构造大矩阵。

## 它为什么重要
在深度网络中，Jacobian/Hessian 直接计算代价很高，随机估计法能显著降本。

## 一个小例子
想估计某矩阵相关统计量时，不直接展开矩阵，而是采样若干 Rademacher 向量做向量乘积并取平均。

## 更正式的定义
Hutchinson Estimator 是基于随机向量（常用 Rademacher）构造的随机估计器，用于近似矩阵迹或相关统计。

## 数学形式（如有必要）
对对称矩阵 `A`，若随机向量 `v` 满足 `E[vv^T]=I`，则：
\[
E[v^TAv]=\mathrm{tr}(A)
\]

## 核心要点
1. 用向量乘法替代矩阵显式构造。
2. 采样越多，估计越稳定。
3. 常见于大模型二阶/谱相关近似。

## 这篇论文里怎么用
- [[AZ-NAS]]: 通过 Rademacher 向量近似 Jacobian 相关量，构造可训练性 proxy。

## 代表工作
- Avron and Toledo, JACM 2011.

## 相关概念
- [[Spectral Norm]]
- [[Zero-Cost Proxy]]

