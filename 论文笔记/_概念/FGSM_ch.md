---
type: concept
language: zh-CN
source_concept_note: "[[FGSM]]"
aliases: [快速梯度符号法, FGSM]
---

# FGSM 中文条目

## 一句话直觉
FGSM 用一次梯度符号步就能构造对抗样本：沿着让损失增大的方向，把输入每个维度推 `eps`。

## 它为什么重要
它是最经典、最便宜的对抗攻击/对抗训练基线之一。

## 一个小例子
某像素梯度为正就加 `+eps`，梯度为负就减 `-eps`，一次更新得到对抗样本。

## 更正式的定义
\[
x_{adv}=x+\epsilon\cdot \mathrm{sign}(\nabla_x L(f_\theta(x),y))
\]

## 数学形式（如有必要）
`eps` 控制 `l_inf` 范数下的扰动预算。

## 核心要点
1. 一步攻击，速度快。
2. 强度通常弱于多步 PGD。
3. 配合随机初始化可提升训练稳定性。

## 这篇论文里怎么用
- [[ABanditNAS]]: 搜索阶段和训练设置中使用 FGSM + 随机初始化来降低开销。

## 代表工作
- Goodfellow et al. (2014): FGSM 起源论文。
- Wong et al. (2020): 快速对抗训练相关改进。

## 相关概念
- [[PGD Attack]]
- [[Adversarial Robustness]]
- [[ABanditNAS]]

