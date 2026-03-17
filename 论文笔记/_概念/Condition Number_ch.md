---
type: concept
language: zh-CN
source_concept_note: "[[Condition Number]]"
aliases: [条件数, Matrix Condition Number]
---

# Condition Number 中文条目

## 一句话直觉
条件数衡量“输入轻微变化会被放大多少”，数值越大通常越不稳定。

## 它为什么重要
它连接了矩阵几何结构与优化数值稳定性，是判断特征是否“健康”的关键指标。

## 一个小例子
当两列特征几乎平行时，最小奇异值会非常小，条件数迅速变大，说明后续计算对噪声很敏感。

## 更正式的定义
谱条件数定义为：
\[
c(X)=\frac{\sigma_{\max}(X)}{\sigma_{\min}(X)}
\]
其中 \(\sigma_{\max}\) 和 \(\sigma_{\min}\) 是最大/最小奇异值。

## 数学形式（如有必要）
- 条件好：\(c(X)\) 接近 1。
- 条件差：\(c(X)\) 很大。
- 逆条件数信号：\(1/c(X)=\sigma_{\min}/\sigma_{\max}\)。

## 核心要点
1. 最小奇异值太小是条件差的核心原因。
2. 条件数可视为“共线性强弱”的量化指标。
3. 在 training-free NAS 中，逆条件数常用来衡量特征多样性。

## 这篇论文里怎么用
- [[Dextr]]: 跨层汇总逆条件数项，并与曲率项融合形成最终代理分数。

## 代表工作
- [[Dextr]]: 将条件数侧作为收敛/泛化分量。
- [[MeCo]]: 谱与相关结构驱动的训练前代理路线。

## 相关概念
- [[Singular Value Decomposition]]
- [[Gram Matrix]]
- [[Feature Map Collinearity]]

