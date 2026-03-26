---
type: concept
language: zh-CN
source_concept_note: "[[Synaptic Flow]]"
aliases: [突触流, SynFlow]
---

# Synaptic Flow 中文条目

## 一句话直觉
Synaptic Flow（SynFlow）是在“未训练状态”下给网络打分的零成本代理，用来估计架构的潜在可学习性。

## 它为什么重要
在 NAS 中，SynFlow 可以极低成本筛掉大量差架构，减少完整训练评测次数。

## 一个小例子
两个模型 FLOPs 接近时，若 A 的 SynFlow 明显高于 B，搜索器通常会优先继续评估 A。

## 更正式的定义
SynFlow 通过合成输入与参数敏感度计算每个权重的贡献，再把全网贡献聚合为架构分数。

## 数学形式（如有必要）
\[
\text{SynFlow}(w) = \left| \frac{\partial L}{\partial w} \odot w \right|
\]
其中 \(L\) 是合成损失，\(\odot\) 表示逐元素乘积。

## 核心要点
1. 训练自由，可在训练前计算。
2. 常用于排序代理，不是准确率本体。
3. 高 SynFlow 不必然等于最高对抗鲁棒性。

## 这篇论文里怎么用
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 将 SynFlow 作为 GA/NSGA-II 的训练自由搜索目标。

## 代表工作
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: 在对抗训练评测条件下重新检验 SynFlow 有效性。

## 相关概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]

