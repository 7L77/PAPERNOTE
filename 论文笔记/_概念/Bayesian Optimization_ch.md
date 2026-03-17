---
type: concept
language: zh-CN
source_concept_note: "[[Bayesian Optimization]]"
aliases: [贝叶斯优化, Bayesian Optimization]
---

# Bayesian Optimization 中文条目

## 一句话直觉
Bayesian Optimization（BO）是在“每次评估都很贵”的场景下，用一个便宜的代理模型指导下一次该试什么。

## 它为什么重要
在 NAS 里，真实训练一个候选架构成本很高；BO 能用更少的真实训练次数找到更优解。

## 一个小例子
你只能训练 20 个候选架构。BO 会根据已训练结果拟合代理模型，优先尝试“预测好且不确定性高”的候选点。

## 更正式的定义
BO 通过“概率代理模型 + 采集策略”迭代选择下一个真实评估点，以在有限预算下优化黑盒目标函数。

## 核心要点
1. 适合高成本黑盒优化。
2. 关键在探索与利用平衡。
3. 代理模型校准质量决定效果上限。

## 这篇论文里怎么用
- [[PO-NAS]]: 在每轮迭代中，用有限真实性能反馈更新代理模型，再选择下一批候选架构进行真实训练。

## 代表工作
- [[BOHB]]: BO 与 bandit 结合。
- [[BANANAS]]: 面向 NAS 的 BO 风格代理优化。

## 相关概念
- [[Surrogate Predictor]]
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]
