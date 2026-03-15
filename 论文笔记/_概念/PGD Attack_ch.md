---
type: concept
language: zh-CN
source_concept_note: "[[PGD Attack]]"
aliases: [投影梯度下降攻击, PGD]
---

# PGD Attack 中文条目

## 一句话直觉
PGD 通过“多次小步梯度上升 + 每步投影回扰动约束集合”来持续强化对抗扰动。

## 它为什么重要
它是鲁棒学习里最常用的强一阶攻击评测标准之一。

## 一个小例子
从随机扰动起点出发，做 7/20/40 次更新，每步后都 clip 回 `eps` 半径的 `l_inf` 球。

## 更正式的定义
\[
x_{t+1}=\Pi_{B_\epsilon(x)}\big(x_t+\alpha\cdot \mathrm{sign}(\nabla_x L(f_\theta(x_t),y))\big)
\]

## 数学形式（如有必要）
步数越多通常攻击越强，但计算代价也越高。

## 核心要点
1. 是 FGSM 的多步强化版本。
2. 常见设置有 PGD-7/20/40/100。
3. 可配合随机重启提升攻击强度。

## 这篇论文里怎么用
- [[ABanditNAS]]: 以 PGD 作为核心鲁棒评测（CIFAR-10 报告 PGD-7/20，MNIST 报告 PGD-40/100）。

## 代表工作
- Madry et al. (2017): PGD 对抗训练经典工作。
- Kurakin et al. (2016): 迭代型攻击相关工作。

## 相关概念
- [[FGSM]]
- [[Adversarial Robustness]]
- [[ABanditNAS]]

