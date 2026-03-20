---
type: concept
language: zh-CN
source_concept_note: "[[Neural Graph Features (GRAF)]]"
aliases: [GRAF, 神经网络图特征]
---

# Neural Graph Features (GRAF) 中文条目

## 一句话直觉
GRAF 把网络架构当作图来描述，用拓扑统计特征（如路径长度、路径允许算子）补充传统 zero-cost 代理。

## 它为什么重要
只看 ZCP 可能忽略结构信息。GRAF 可以提供“连通结构层面”的额外证据，常用于提升预测稳定性。

## 一个小例子
两个候选 cell 的 `jacov` 很接近，但一个路径更短、跳连更多，另一个路径更深。GRAF 特征可以把这两者区分开。

## 更正式的定义
Neural Graph Features 是从神经架构图中提取的拓扑描述符，用于增强架构性能预测模型的输入特征。

## 核心要点
1. 显式编码架构拓扑，而非只看梯度/权重统计。
2. 更适合作为 ZCP 的补充特征，而不是完全替代。
3. 在代理特征不充分时，常带来可观增益。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 在代理向量后拼接 191 维 GRAF，Table 6/7 显示多数鲁棒设置有提升。

## 代表工作
- Kadlecova et al. (2024): 在 NAS 中提出/系统化 GRAF 特征。
- [[ZCP-Eval]]: 评估 GRAF 与 ZCP 联合用于鲁棒预测。

## 相关概念
- [[Zero-Cost Proxy]]
- [[NAS-Bench-201]]
- [[Cell-based Search Space]]
