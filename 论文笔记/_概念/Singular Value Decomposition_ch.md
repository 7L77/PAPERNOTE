---
type: concept
language: zh-CN
source_concept_note: "[[Singular Value Decomposition]]"
aliases: [奇异值分解, SVD]
---

# Singular Value Decomposition 中文条目

## 一句话直觉
SVD 可以把一个矩阵拆成“旋转 + 轴向拉伸”，从而看清它真正有效的信息方向和强度。

## 它为什么重要
在神经网络分析里，SVD 常用来判断特征是否退化、是否共线、数值是否稳定，以及表示的有效维度。

## 一个小例子
如果某层特征矩阵只有一个奇异值很大，其余都很小，说明大多数信息都挤在一个方向上，表示很容易塌缩。

## 更正式的定义
对矩阵 \(X\in\mathbb{R}^{m\times n}\)：
\[
X=U\Sigma V^\top
\]
其中 \(U,V\) 为正交矩阵，\(\Sigma\) 的对角线是按降序排列的奇异值。

## 数学形式（如有必要）
- 条件数：\(c(X)=\sigma_{\max}/\sigma_{\min}\)。
- 常见逆条件数信号：\(\sigma_{\min}/\sigma_{\max}=1/c(X)\)。

## 核心要点
1. 奇异值谱能直接反映表示的有效维度与稳定性。
2. 条件数大通常意味着共线性强、数值不稳定。
3. 用激活特征做 SVD 不需要标签，适合训练前 proxy。

## 这篇论文里怎么用
- [[Dextr]]: 对层特征做 SVD，取逆条件数信号作为收敛/泛化侧分数的一部分。

## 代表工作
- [[Dextr]]: SVD + 曲率融合的 zero-shot NAS proxy。
- [[W-PCA]]: 通过谱结构信息构建 training-free 指标。

## 相关概念
- [[Condition Number]]
- [[Gram Matrix]]
- [[Network Expressivity]]

