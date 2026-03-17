---
type: concept
language: zh-CN
source_concept_note: "[[Hessian Spectrum]]"
aliases: [Hessian Spectrum, Hessian 谱]
---

# Hessian Spectrum 中文条目

## 一句话直觉
Hessian 谱刻画损失曲面的弯曲程度，最大特征值越大通常表示曲面更尖、对扰动更敏感。

## 它为什么重要
它是常见鲁棒性代理信号，可用于快速判断网络在输入扰动下的稳定性趋势。

## 一个小例子
同样大小的扰动，陡峭山谷（大特征值）更容易让损失剧烈变化，平缓山谷（小特征值）变化较小。

## 更正式的定义
设损失函数为 `L`，Hessian 为 `H`。`H` 的最大特征值 `lambda_max(H)` 常用来表示局部曲率强度。

## 数学形式（如有必要）
\[
\lambda_{\max}(H) = \max_{\|v\|_2=1} v^\top H v.
\]

## 核心要点
1. 谱信息反映局部敏感性。
2. 最大特征值是最常见的单值摘要。
3. 与真实鲁棒性的相关性会随攻击强度变化。

## 这篇论文里怎么用
- [[NADR-Dataset]]: 在全架构空间计算 Hessian 最大特征值，并与鲁棒排名做 Kendall 相关性比较。

## 代表工作
- Zhao et al., 2020.
- Mok et al., 2021.

## 相关概念
- [[Jacobian Norm Bound]]
- [[Adversarial Robustness]]
- [[NADR-Dataset]]

