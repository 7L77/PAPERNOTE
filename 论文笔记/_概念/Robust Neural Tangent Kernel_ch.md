---
type: concept
language: zh-CN
source_concept_note: "[[Robust Neural Tangent Kernel]]"
aliases: [鲁棒神经切线核, Robust NTK]
---

# Robust Neural Tangent Kernel 中文条目

## 一句话直觉
Robust NTK 是把 NTK 从“干净样本几何”扩展到“对抗样本几何”，用于解释对抗训练下的学习与泛化行为。

## 它为什么重要
在 robust NAS 里，只看 clean 信号容易把架构排错序；Robust NTK 往往与鲁棒精度更一致，因此更适合作为鲁棒搜索线索。

## 一个小例子
两个架构 clean NTK 分数相近，但在对抗扰动后 A 的 robust NTK 更高，最终在 PGD 指标下 A 往往更靠前。

## 更正式的定义
给定攻击器 `A_eps`，用扰动后的样本构建核：
- clean 核: `K(i,j)=k(x_i,x_j)`
- robust 核: `K_tilde_eps(i,j)=k(A_eps(x_i),A_eps(x_j))`
- 还可加入 clean 与扰动样本之间的 cross 项。

在 [[NAS-RobBench-201]] 中，最终用于泛化界的是 clean/cross/robust 的加权混合核。

## 数学形式（如有必要）
\[
K_{all} = (1-\beta)^2 K + \beta(1-\beta)(\bar{K}_{\epsilon} + \bar{K}_{\epsilon}^{\top}) + \beta^2 \tilde{K}_{\epsilon}
\]
\[
\tilde{K}_{all} = (1-\beta)^2 \tilde{K}_{\epsilon} + \beta(1-\beta)(\bar{K}_{2\epsilon} + \bar{K}_{2\epsilon}^{\top}) + \beta^2 \tilde{K}_{2\epsilon}
\]

其中 `beta` 是 clean/robust 权衡系数。  
Source: [[NAS-RobBench-201]] Eq. (4)-(5).

## 核心要点
1. Robust NTK 是 NTK 的鲁棒扩展，而不是简单换名。
2. 在对抗训练语境下，它与鲁棒精度的相关性通常高于 clean NTK。
3. 与 twice perturbation 结合时，可更好刻画强扰动场景。

## 这篇论文里怎么用
- [[NAS-RobBench-201]]：用混合核最小特征值相关量给出 clean/robust 泛化界。

## 代表工作
- [[NAS-RobBench-201]]：多目标对抗训练下 robust/mixed NTK 的理论化。
- [[TRNAS]]：在实践中使用 NTK 相关信号指导鲁棒搜索。

## 相关概念
- [[Neural Tangent Kernel]]
- [[Twice Perturbation]]
- [[Multi-objective Adversarial Training]]
- [[Adversarial Robustness]]

