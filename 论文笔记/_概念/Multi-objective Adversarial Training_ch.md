---
type: concept
language: zh-CN
source_concept_note: "[[Multi-objective Adversarial Training]]"
aliases: [多目标对抗训练, Clean-Robust 联合目标]
---

# Multi-objective Adversarial Training 中文条目

## 一句话直觉
多目标对抗训练同时优化 clean 与 robust 两类目标，而不是只追一个指标。

## 它为什么重要
robust NAS 的核心就是“精度-鲁棒性”权衡，这个目标函数把权衡参数显式化，方便比较与调参。

## 一个小例子
当 `beta=0` 时只看 clean loss；`beta=1` 时只看 robust loss；中间值代表两者折中。

## 更正式的定义
\[
\mathcal{L}(W)=(1-\beta)\mathcal{L}_{clean}(W)+\beta \mathcal{L}_{robust}(W), \quad \beta\in[0,1].
\]
其中 `L_clean` 是标准样本损失，`L_robust` 是对抗样本损失。

## 数学形式（如有必要）
\[
\mathcal{L}_{robust}(W)=\frac{1}{N}\sum_{i=1}^{N}\ell\big(y_i,f(A_{\epsilon}(x_i,W),W)\big)
\]

在 [[NAS-RobBench-201]] 中，该目标不仅用于训练，也用于后续 NTK 泛化界推导。  
Source: [[NAS-RobBench-201]] Eq. (3), Sec. 4.1.

## 核心要点
1. `beta` 直接控制 clean/robust 取舍。
2. 目标函数形态会影响架构排名与理论核定义。
3. 它把经验 robust NAS 与理论分析连接起来。

## 这篇论文里怎么用
- [[NAS-RobBench-201]]：用该目标定义 benchmark 训练过程，并推导 clean/robust bound。

## 代表工作
- [[NAS-RobBench-201]]：基准构建 + 理论推导同源于该目标。
- [[AdvRush]]：在 robust NAS 中加入面向鲁棒性的额外优化项。

## 相关概念
- [[Adversarial Robustness]]
- [[Robust Neural Tangent Kernel]]
- [[PGD Attack]]
- [[Robust Neural Architecture Search]]

