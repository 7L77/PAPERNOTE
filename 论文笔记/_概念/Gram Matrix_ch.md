---
type: concept
language: zh-CN
source_concept_note: "[[Gram Matrix]]"
aliases: [格拉姆矩阵, Kernel Gram Matrix]
---

# Gram Matrix 中文条目

## 一句话直觉
Gram 矩阵记录向量两两内积，本质上是在描述“彼此有多像”。

## 它为什么重要
它的谱（尤其最小特征值）常用于分析优化收敛与泛化，是核方法/NTK 理论里的核心对象。

## 一个小例子
如果很多特征向量几乎平行，Gram 矩阵会接近奇异，说明信息方向重复、表示多样性不足。

## 更正式的定义
给定向量 \(x_1,\dots,x_n\)，Gram 矩阵 \(G\) 定义为：
\[
G_{ij}=x_i^\top x_j
\]
更一般可写为核形式 \(G_{ij}=k(x_i,x_j)\)。

## 数学形式（如有必要）
- Gram 矩阵是半正定的（\(G\succeq0\)）。
- \(\lambda_{\min}(G)\) 很小时，通常表示条件差、方向区分弱。

## 核心要点
1. Gram 矩阵是样本几何关系的紧凑表示。
2. 特征值谱能反映秩、信息多样性与稳定性。
3. 在 NAS 代理理论里，它常被用于解释可训练性与泛化趋势。

## 这篇论文里怎么用
- [[Dextr]]: 理论上借助 Gram/NTK 最小特征值与收敛/泛化关系，再在实现中用层特征条件数近似该信号。

## 代表工作
- [[Dextr]]: 将 Gram 侧理论动机映射到可计算的 SVD 层评分。
- [[Neural Tangent Kernel]]: 通过核 Gram 矩阵分析训练动力学。

## 相关概念
- [[Condition Number]]
- [[Singular Value Decomposition]]
- [[Neural Tangent Kernel]]

