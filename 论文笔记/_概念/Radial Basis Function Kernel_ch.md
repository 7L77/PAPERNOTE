---
type: concept
language: zh-CN
source_concept_note: "[[Radial Basis Function Kernel]]"
aliases: [RBF核, 高斯核]
---

# Radial Basis Function Kernel 中文条目

## 一句话直觉
RBF 核把“距离”变成“相似度”：距离越近，相似度越接近 1；距离越远，相似度越接近 0。

## 它为什么重要
很多模型需要比较样本相似性，RBF 核可以用一个简单公式建模非线性关系。

## 一个小例子
两个特征向量几乎相同，`exp(-gamma*||x-y||^2)` 会很大；差异很大时会快速变小。

## 更正式的定义
\[
K_{ij}=\exp(-\gamma \|x_i-x_j\|^2),\quad \gamma>0
\]
其中 `gamma` 控制衰减速度与敏感度。

## 核心要点
1. `gamma` 太大时，核值容易饱和到接近 0。
2. `gamma` 太小时，样本间差异被压平。
3. 在“距离有语义”的表征空间里效果通常较好。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 分别对激活输出和最后层输入特征图构建 RBF 相似矩阵。
- 再用行列式相关量聚合得到架构评分。

## 代表工作
- [[RBFleX-NAS]]: 双 RBF 核用于 training-free NAS 评分。

## 相关概念
- [[Kronecker Product]]
- [[Hyperparameter Detection Algorithm]]
- [[Zero-Cost Proxy]]

