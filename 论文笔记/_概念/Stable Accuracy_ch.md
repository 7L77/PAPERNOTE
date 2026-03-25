---
type: concept
language: zh-CN
source_concept_note: "[[Stable Accuracy]]"
aliases: [稳定准确率, Stable Accuracy]
---

# Stable Accuracy 中文条目

## 一句话直觉
Stable Accuracy 关注的是“攻击后预测有没有变”，而不只是“最后答对没答对”。

## 它为什么重要
在鲁棒性研究里，它能更直接反映模型对扰动的预测稳定性，常用于解释为何某些架构更鲁棒。

## 一个小例子
样本干净输入时预测为 A，被攻击后仍预测 A，则记为 stable。  
若被攻击后从 A 变为 B，则不 stable。

## 更正式的定义
对数据集 `D`、模型 `f` 与攻击后样本 `x_hat`，Stable Accuracy 定义为：
`|{x in D : f(x) = f(x_hat)}| / |D|`。

## 数学形式（如有必要）
\[
\text{StableAcc}=\frac{\left|\{x \in D:\ f(x)=f(\hat{x})\}\right|}{|D|}
\]

## 核心要点
1. 它衡量的是“预测是否保持不变”。
2. 与鲁棒准确率互补，适合做训练过程诊断。
3. 有时比 clean accuracy 更能指示鲁棒架构趋势。

## 这篇论文里怎么用
- [[NARes]]: 把 Stable Accuracy 作为核心诊断指标，做了全空间统计并与鲁棒精度关系分析。

## 代表工作
- [[NARes]]: 在大规模 WRN 架构空间中系统记录并分析该指标。
- Wu et al. (2021): 强调稳定性视角对理解对抗训练的重要性。

## 相关概念
- [[Adversarial Robustness]]
- [[PGD Attack]]
- [[Lipschitz Constant]]

