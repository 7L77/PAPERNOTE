---
type: concept
language: zh-CN
source_concept_note: "[[Generalized Zero-Shot Learning]]"
aliases: [广义零样本学习, GZSL]
---

# Generalized Zero-Shot Learning 中文条目

## 一句话直觉
Generalized Zero-Shot Learning（GZSL）要求模型在测试时同时识别 seen 和 unseen 类别，比普通 ZSL 更难、更接近真实场景。

## 它为什么重要
真实数据流不会只包含 unseen 类，GZSL 能检验模型是否“只会偏向 seen 类”。

## 一个小例子
测试集同时出现马（seen）和霍加狓（unseen）。如果模型总预测 seen 类，即使 seen 精度高，也会导致 GZSL 指标差。

## 更正式的定义
训练阶段 seen/unseen 类别互斥，测试阶段在 `Y_s ∪ Y_u` 上联合分类。常用指标是 `A_s`（seen 准确率）、`A_u`（unseen 准确率）和调和平均 `A_h`。

## 核心要点
1. GZSL 关注 seen/unseen 的平衡，不是只看 unseen。
2. `A_h` 对类别偏置非常敏感。
3. 评估时应同时报告 `A_s`、`A_u` 和 `A_h`。

## 这篇论文里怎么用
- [[ZeroNAS]]: 在 CUB/FLO/SUN/AWA 上报告 GZSL 结果，并展示架构搜索可改善 `A_s` 与 `A_u` 的平衡。

## 代表工作
- [[ZeroNAS]]: 用搜索后的 GAN 架构提升 GZSL 指标。

## 相关概念
- [[Zero-Shot Learning]]
- [[Generative Adversarial Network]]
- [[Neural Architecture Search]]

