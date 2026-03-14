---
type: concept
language: zh-CN
source_concept_note: "[[Robust Neural Architecture Search]]"
aliases: [鲁棒NAS, 鲁棒性架构搜索]
---

# Robust Neural Architecture Search 中文条目

## 一句话直觉
Robust NAS 不只追求 clean accuracy，还要在攻击或分布扰动下保持性能。

## 它为什么重要
实际系统里，“高精度但一攻击就崩”的网络价值有限，鲁棒性必须进入架构搜索目标。

## 一个小例子
在自动驾驶场景下，宁可选 clean 略低但 PGD 鲁棒性更高的架构。

## 更正式的定义
Robust NAS 是把鲁棒性作为目标或约束的神经架构搜索，通常采用单目标 robust 或 clean+robust 多目标联合优化。

## 核心要点
1. 鲁棒评估成本高于 clean 评估。
2. 常见设定是 clean 与 robust 的多目标权衡。
3. 低成本代理预测对可扩展 robust NAS 很关键。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 研究传统 ZCP 能否迁移为鲁棒性能预测器。

## 代表工作
- [[ZCP-Eval]]: 证明鲁棒预测通常依赖多代理特征融合。
- [[Adversarially Robust Architecture Search]]: 早期鲁棒 NAS 路线。

## 相关概念
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]

