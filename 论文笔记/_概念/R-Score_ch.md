---
type: concept
language: zh-CN
source_concept_note: "[[R-Score]]"
aliases: [鲁棒评分, 鲁棒代理分数]
---

# R-Score 中文条目

## 一句话直觉
R-Score 是 TRNAS 提出的训练前鲁棒性代理分数，用来在不做完整对抗训练时先判断架构的鲁棒潜力。

## 它为什么重要
鲁棒 NAS 的主要成本在“候选架构都要对抗训练”。R-Score 让我们先做低成本筛选，再把预算集中给少量高潜力架构。

## 一个小例子
若两个候选 clean 指标接近，但 A 的 R-Score 更高，TRNAS 会优先保留 A 进入后续进化与最终训练。

## 更正式的定义
R-Score 由两部分组成:
1. 线性激活能力（LAM，偏局部扰动敏感性）；
2. 特征一致性（FRM，偏全局稳定性）。
最终加权求和:
`R = beta * LAM + (1 - beta) * FRM`。

## 核心要点
1. 目标是鲁棒排序，不是普通 clean 排序。
2. 在训练前阶段即可计算。
3. 通常与多目标选择策略联合使用，提升搜索稳定性。

## 这篇论文里怎么用
- [[TRNAS]] 在 DARTS 搜索空间中用 R-Score 做候选打分和筛选。

## 代表工作
- [[TRNAS]]: 提出并使用 R-Score 的训练前鲁棒 NAS 方法。

## 相关概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[RobustBench]]

