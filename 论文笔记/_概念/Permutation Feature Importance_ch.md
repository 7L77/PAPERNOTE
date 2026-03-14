---
type: concept
language: zh-CN
source_concept_note: "[[Permutation Feature Importance]]"
aliases: [置换特征重要性, PFI]
---

# Permutation Feature Importance 中文条目

## 一句话直觉
把某个特征随机打乱后，如果模型性能明显变差，说明这个特征重要。

## 它为什么重要
它是模型无关的解释方法，能直接回答“这个特征被破坏后模型会掉多少分”。

## 一个小例子
随机打乱 `jacov` 后 R2 大幅下降，而打乱 `zen` 几乎不变，就说明 `jacov` 对当前任务更关键。

## 更正式的定义
固定已训练模型，对单个特征做随机置换并比较性能下降幅度，该下降的期望值可作为该特征的重要性度量。

## 核心要点
1. 适用于多种模型，不局限树模型。
2. 重要性随任务与数据分布变化。
3. 特征相关性强时，重要性会被“分摊”。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 用置换重要性分析证明鲁棒预测需要多代理组合。

## 代表工作
- [[Breiman Random Forests]]: 树模型解释中的经典背景。
- [[ZCP-Eval]]: 在 NAS 鲁棒预测场景中的应用。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Surrogate Predictor]]
- [[Robust Neural Architecture Search]]

