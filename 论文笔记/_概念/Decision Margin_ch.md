---
type: concept
language: zh-CN
source_concept_note: "[[Decision Margin]]"
aliases: [决策间隔, Logit Margin]
---

# Decision Margin 中文条目

## 一句话直觉

Decision Margin（决策间隔）就是“真实类别分数比第二名高多少”；差距越小，样本越容易被扰动翻转。

## 它为什么重要

在鲁棒学习里，它是判断样本是否靠近决策边界的直接指标，也是很多样本加权/筛选策略的基础。

## 一个小例子

某样本 logits 为 `[cat=4.2, dog=3.9, bird=0.8]`，标签是 `cat`，间隔为 `0.3`。  
如果扰动把 `dog` 抬高一点，预测就可能从 `cat` 变成 `dog`。

## 更正式的定义

对样本 \(x\) 与真标签 \(y\)，决策间隔定义为：
\[
M_\theta^y(x)=\ell_\theta^y(x)-\max_{y'\neq y}\ell_\theta^{y'}(x)
\]
其中 \(\ell_\theta^c(x)\) 是类别 \(c\) 的 logit。

## 数学形式（如有必要）

当间隔明显为正且较大时，通常表示样本离当前决策边界更远。

## 核心要点

1. 它是“样本级、模型状态级”的动态量。
2. 会随训练阶段和攻击方式变化。
3. clean/adv 的间隔差可用于估计样本脆弱性。

## 这篇论文里怎么用

- [[VDAT]]: 用 clean 与 adversarial 的 margin 差来构造 vulnerability 分数。

## 代表工作

- [[VDAT]]: 用 margin shift 驱动样本级对抗训练筛选。
- [[Robust Principles]]: 从架构视角讨论与边界相关的鲁棒性行为。

## 相关概念

- [[Adversarial Training]]
- [[PGD Attack]]

