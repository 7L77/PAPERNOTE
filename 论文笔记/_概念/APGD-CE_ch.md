---
type: concept
language: zh-CN
source_concept_note: "[[APGD-CE]]"
aliases: [自动步长PGD-交叉熵, Auto-PGD CE]
---

# APGD-CE 中文条目

## 一句话直觉
APGD-CE 是一种会自动调步长的多步 PGD 攻击，用交叉熵目标来找更强的对抗样本。

## 它为什么重要
相比单步攻击（如 FGSM），APGD-CE 更强、更稳定，是鲁棒性评测中的常用强基线。

## 一个小例子
同样的 epsilon 预算下，FGSM 可能失败，但 APGD-CE 通过多步迭代和投影常能成功攻击模型。

## 更正式的定义
APGD-CE 通过“梯度更新 + 投影回 epsilon-ball + 自适应步长”迭代求解约束内最大化交叉熵损失的优化问题。

## 核心要点
1. 是强白盒攻击，不是训练方法。
2. 每一步都投影回约束球，保证扰动预算不超限。
3. CE 和 DLR 等不同目标函数会影响攻击效果。

## 这篇论文里怎么用
- [[Padding-Robustness Interplay]]: 论文里 APGD-CE 既单独报告，也作为 AutoAttack 一部分；zero padding 在该攻击下经常占优。

## 代表工作
- [[AutoAttack]]: 将 APGD 系列整合进标准化鲁棒评估流程。

## 相关概念
- [[AutoAttack]]
- [[Adversarial Robustness]]

