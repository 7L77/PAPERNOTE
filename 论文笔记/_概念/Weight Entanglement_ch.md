---
type: concept
language: zh-CN
source_concept_note: "[[Weight Entanglement]]"
aliases: [权重纠缠, Weight Entanglement]
---

# Weight Entanglement 中文条目

## 一句话直觉
Weight Entanglement 是把预训练模型里“对得上形状”的参数切片复用到候选架构中，从而避免每个候选都从零训练。

## 它为什么重要
大模型 NAS 的候选很多，完全训练成本极高；权重复用能显著降低构建 NASBench 与代理评估的成本。

## 一个小例子
基于 130M 预训练模型采样一个更窄网络时，直接继承兼容层的权重，再做短时微调，而不是从随机初始化开始。

## 更正式的定义
Weight Entanglement 是一种参数共享初始化策略：候选架构从参考模型继承可对齐参数子集，以降低评估开销。

## 数学形式（如有必要）
可抽象为
\[
\theta_{candidate} \leftarrow \mathcal{S}(\theta_{reference}, A_{candidate})
\]
其中 `\mathcal{S}` 表示按架构约束进行参数切片与对齐。

## 核心要点
1. 主要收益是降本提速。
2. 代价是可能引入性能观测噪声。
3. 这类噪声通常会让相关性估计更保守。

## 这篇论文里怎么用
- [[TF-MAS]]: 用该策略构建 Mamba2 NASBench，并通过短时 fine-tuning 获得候选性能用于相关性评估。

## 代表工作
- [[TF-MAS]]: 在 Mamba2 大规模候选评估中采用该策略。

## 相关概念
- [[Super-network]]
- [[Evolutionary Neural Architecture Search]]
- [[Training-free NAS]]

