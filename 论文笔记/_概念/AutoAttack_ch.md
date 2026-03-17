---
type: concept
language: zh-CN
source_concept_note: "[[AutoAttack]]"
aliases: [AA, AutoAttack]
---

# AutoAttack 中文条目

## 一句话直觉
AutoAttack 是一组标准化对抗攻击协议，用来更可靠地评估模型真实鲁棒性。

## 它为什么重要
只报单一攻击结果容易“看起来很强”；AA 通过组合攻击减少评估偏差。

## 一个小例子
模型在某个 PGD 配置下很高分，但在 AA 下可能出现明显下降，说明鲁棒性被高估了。

## 更正式的定义
AutoAttack 是固定的多攻击组合评估流程，强调少调参、可比较、可复核。

## 核心要点
1. 强调评估协议标准化。
2. 常作为鲁棒论文主指标。
3. 建议与 PGD 指标一起看。

## 这篇论文里怎么用
- [[Robust Principles]]: 把 AA 作为主要鲁棒指标报告，并给出 1-9pp 的提升区间。

## 代表工作
- [[Robust Principles]]: 在 CIFAR/ImageNet 上报告 AA 改进结果。

## 相关概念
- [[PGD Attack]]
- [[RobustBench]]

