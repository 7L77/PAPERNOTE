---
type: concept
language: zh-CN
source_concept_note: "[[Adversarial Robustness]]"
aliases: [对抗鲁棒性, 对抗攻击鲁棒性]
---

# Adversarial Robustness 中文条目

## 一句话直觉
对抗鲁棒性是指模型在“被恶意微扰”的输入上仍能保持正确预测的能力。

## 它为什么重要
很小的人眼几乎不可见扰动就可能让模型高置信度误判，部署时风险很高。

## 一个小例子
原图识别为“猫”，加上极小 PGD 扰动后变成“卡车”，说明对抗鲁棒性差。

## 更正式的定义
在给定扰动约束（如 Linf 的 epsilon）下，模型在最坏情况输入上的准确率或错误率度量，称为对抗鲁棒性。

## 核心要点
1. clean accuracy 高不等于鲁棒性高。
2. 不同攻击（FGSM/PGD/APGD/AutoAttack）下鲁棒性表现不同。
3. 鲁棒评估通常比 clean 评估更耗时。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 把鲁棒准确率当作代理预测目标，比较不同 ZCP 的迁移能力。

## 代表工作
- [[Explaining and Harnessing Adversarial Examples]]: 对抗样本经典工作。
- [[AutoAttack]]: 常用强攻击评测套件。

## 相关概念
- [[Robust Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]

