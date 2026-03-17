---
type: concept
language: zh-CN
source_concept_note: "[[Robust Search Objective]]"
aliases: [鲁棒搜索目标, Robust Search Objective]
---

# Robust Search Objective 中文条目

## 一句话直觉

它是把 clean 损失和多强度对抗损失加权成一个可优化标量的目标函数，用来指导架构搜索。

## 它为什么重要

没有统一目标，搜索很容易偏向某一端（只顾 clean 或只顾某个强攻击点）。鲁棒搜索目标能明确表达权衡关系。

## 一个小例子

两个架构 clean 表现接近时，若其中一个在多个强度上的加权对抗损失更低，它会在搜索中被优先保留。

## 更正式的定义

典型形式：
\[
\mathcal{J}(A)=\alpha \hat{L}_{natural}(A)+\beta\sum_i \beta_i \hat{L}_{\epsilon_i}(A),
\]
满足 \(\alpha+\beta=1\)、\(\sum_i\beta_i=1\)。

## 数学形式（如有必要）

在 Wsr-NAS 中，这个目标由 VLE 预测到的多头验证损失驱动架构参数更新。

## 核心要点

1. \(\alpha,\beta\) 控制整体 clean/robust 权衡。
2. \(\beta_i\) 控制不同攻击强度的关注程度。
3. 权重归一化对训练稳定性和可解释性很关键。

## 这篇论文里怎么用

- [[Wsr-NAS]]: 用 Eq.(10) 聚合 clean 与多强度损失来更新超网架构参数。

## 代表工作

- [[Wsr-NAS]]: 将多强度鲁棒目标与轻量损失估计器结合用于 robust NAS。

## 相关概念

- [[Validation Loss Estimator]]
- [[Wide Spectrum Adversarial Robustness]]
- [[One-shot NAS]]
- [[Adversarial Robustness]]

