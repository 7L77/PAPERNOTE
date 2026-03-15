---
type: concept
language: zh-CN
source_concept_note: "[[Common Corruptions]]"
aliases: [常见腐化扰动, 自然腐化]
---

# Common Corruptions 中文条目

## 一句话直觉
Common corruptions 指噪声、模糊、天气、数字伪影等“自然但会降质”的输入扰动。

## 为什么重要
真实部署中模型常遇到分布漂移，不能只看 clean accuracy 或单一对抗攻击。

## 小例子
一个模型在 clean CIFAR-10 很高分，但在 fog / Gaussian noise / motion blur 下可能大幅掉点。

## 定义
Common corruptions 是一组标准化自然扰动集合（如 ImageNet-C/CIFAR-C 风格），用于评估模型在真实退化条件下的鲁棒性。

## 关键点
1. 它不是针对单样本优化出的对抗攻击。
2. 更贴近真实场景鲁棒性。
3. 鲁棒 NAS 需要同时关注 adversarial 与 common corruption 两类评测。

## 在本文中的作用
- [[CRoZe]] 在多数据集上同时评估 adversarial attacks 与 15 类 common corruptions。

## 代表工作
- [[CRoZe]]
- [[Robust Neural Architecture Search]]

## 相关概念
- [[Adversarial Robustness]]
- [[Harmonic Robustness Score]]
- [[Neural Architecture Search]]
