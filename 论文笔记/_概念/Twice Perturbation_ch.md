---
type: concept
language: zh-CN
source_concept_note: "[[Twice Perturbation]]"
aliases: [二次扰动, 双重对抗扰动]
---

# Twice Perturbation 中文条目

## 一句话直觉
Twice perturbation 不是“把一次攻击步长调大”，而是“对已经被攻击过的样本再攻击一次”。

## 它为什么重要
这种构造能得到更强的对抗样本分布，有助于分析强扰动下的鲁棒泛化行为；在该论文中用于定义 twice-robust NTK 项。

## 一个小例子
先算 `x_adv1 = A_eps(x)`，再算 `x_adv2 = A_eps(x_adv1)`。`x_adv2` 与“一次性更大步长 PGD”通常不同。

## 更正式的定义
给定攻击器 `A_eps`：
- 一次扰动: `x_adv = A_eps(x)`
- 二次扰动: `x_adv2 = A_eps(x_adv)`

论文把基于 `x_adv2` 的核项放入 robust 泛化界推导。

## 数学形式（如有必要）
\[
\hat{x} = A_{\epsilon}(A_{\epsilon}(x))
\]

Source: [[NAS-RobBench-201]] Sec. 4.2（Eq. (5) 后讨论）。

## 核心要点
1. 二次扰动不等价于“单次攻击增大步长”。
2. 它更偏向强攻击视角。
3. 在本文里它直接进入 robust NTK 组合核的定义。

## 这篇论文里怎么用
- [[NAS-RobBench-201]]：用于构建 `\tilde{K}_{all}` 中的 twice-perturbation 核项，并影响 robust bound。

## 代表工作
- [[NAS-RobBench-201]]：明确给出 twice-perturbation 核定义与用途。
- de Jorge et al. (2022)：作为相关现象讨论引用。

## 相关概念
- [[Robust Neural Tangent Kernel]]
- [[PGD Attack]]
- [[Adversarial Robustness]]
- [[Multi-objective Adversarial Training]]

