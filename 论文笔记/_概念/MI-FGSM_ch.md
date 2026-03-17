---
type: concept
language: zh-CN
source_concept_note: "[[MI-FGSM]]"
aliases: [MI-FGSM, 动量迭代 FGSM]
---

# MI-FGSM 中文条目

## 一句话直觉

MI-FGSM 在多步 FGSM 里加入动量，让攻击方向更稳定、迁移性更强。

## 它为什么重要

相比一步 FGSM，它更强、更可靠，常用于鲁棒性评测基准。

## 一个小例子

每步先把当前梯度和历史动量叠加，再用符号步长更新并投影回扰动预算。

## 更正式的定义

一种带动量项的迭代 `l_inf` 攻击方法。

## 数学形式（如有必要）

`g_{t+1} = mu * g_t + grad_x L / ||grad_x L||_1`，
`x_{t+1} = clip_{x,eps}(x_t + alpha * sign(g_{t+1}))`。

## 核心要点

1. 通常强于一步攻击。
2. 动量可缓解局部梯度噪声。
3. 常和 FGSM/PGD 一起报告。

## 这篇论文里怎么用
- [[RNAS-CL]]: 在 CIFAR-10 表格中报告 MI-FGSM 下的 top-1 鲁棒准确率。

## 代表工作

- Dong et al. (2018): MI-FGSM 原始论文。

## 相关概念

- [[FGSM]]
- [[PGD Attack]]
