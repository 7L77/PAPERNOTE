---
type: concept
language: zh-CN
source_concept_note: "[[Feature Map Collinearity]]"
aliases: [特征图共线性, Feature Collinearity]
---

# Feature Map Collinearity 中文条目

## 一句话直觉
特征图共线性高，表示不同通道在“看同一件事”，新增通道没有带来足够新方向的信息。

## 它为什么重要
共线性高通常意味着有效维度低、条件变差，训练和泛化稳定性都可能受影响。

## 一个小例子
某层 32 个通道几乎都在响应同样的边缘模式，只是幅度不同，这就是典型高共线性。

## 更正式的定义
把层特征图展平成矩阵 \(X_\phi\) 后，如果奇异值谱高度偏斜、最小奇异值很小，则共线性高。

## 数学形式（如有必要）
- 共线性高 \(\Rightarrow \sigma_{\min}(X_\phi)\) 小、条件数 \(c(X_\phi)\) 大。
- 常见多样性信号：\(\sigma_{\min}/\sigma_{\max}=1/c(X_\phi)\)。

## 核心要点
1. 共线性是“表示冗余”的几何刻画。
2. 可在单次前向中无标签估计。
3. 共线性越低，通道多样性通常越高。

## 这篇论文里怎么用
- [[Dextr]]: 将“低共线性”视作更好收敛/泛化的信号，并用逆条件数跨层汇总。

## 代表工作
- [[Dextr]]: 在 zero-shot NAS 中明确讨论特征图共线性与 C/G 的关系。

## 相关概念
- [[Condition Number]]
- [[Singular Value Decomposition]]
- [[Gram Matrix]]

