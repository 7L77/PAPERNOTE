---
type: concept
language: zh-CN
source_concept_note: "[[Surrogate Predictor]]"
aliases: [代理预测器, 代理模型]
---

# Surrogate Predictor 中文条目

## 一句话直觉
代理预测器就是“便宜的打分器”，用来快速估计某个候选架构可能有多好。

## 它为什么重要
NAS 最贵的是反复训练候选网络。代理预测器可以先筛掉差候选，显著节省搜索成本。

## 一个小例子
把架构编码成向量后输入小模型，输出预测精度；只对高分候选再做更贵的评估。

## 更正式的定义
在 NAS 中，Surrogate Predictor 是拟合“架构 -> 性能”的辅助模型，用于近似适应度评估。

## 核心要点
1. 主要作用是降成本。
2. 预测误差会影响候选排序，需要持续校准。
3. 编码质量决定预测上限。

## 这篇论文里怎么用
- [[LLMENAS]]: 在进化环路中使用 `s=g_phi(E(P))` 快速估计候选架构质量。

## 代表工作
- [[NAS-Bench-101]]: 为预测器研究提供标准基准。
- [[BANANAS]]: 结合神经预测器的高效搜索方法。

## 相关概念
- [[One-shot NAS]]
- [[Neural Architecture Search]]
- [[LLM-guided Search]]

