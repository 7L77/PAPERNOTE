---
type: concept
language: zh-CN
source_concept_note: "[[Adversarial Training]]"
aliases: [对抗训练, AT]
---

# Adversarial Training 中文条目

## 一句话直觉
Adversarial Training 就是在训练阶段主动喂给模型“最难的扰动样本”，让模型学会在攻击下也保持正确预测。

## 它为什么重要
它是当前最主流、最有效的一类通用鲁棒训练策略。

## 一个小例子
每个 batch 先用 FGSM/PGD 生成对抗样本，再与干净样本一起训练，目标是两者都分类正确。

## 更正式的定义
对抗训练可写成稳健优化问题：最小化在扰动约束集合内的最坏情况损失，实际中用内层攻击近似求解。

## 核心要点
1. 常提升鲁棒性，但可能牺牲部分 clean accuracy。
2. 训练时使用的攻击类型会影响泛化到其他攻击的效果。
3. 训练成本显著高于普通训练。

## 这篇论文里怎么用
- [[Padding-Robustness Interplay]]: 论文比较普通训练与 FGSM 对抗训练，发现 padding 的优劣排序会随训练方式变化。

## 代表工作
- [[Towards Deep Learning Models Resistant to Adversarial Attacks]]: 经典对抗训练 formulation。

## 相关概念
- [[Adversarial Robustness]]
- [[APGD-CE]]

