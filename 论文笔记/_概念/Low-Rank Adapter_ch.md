---
type: concept
language: zh-CN
source_concept_note: "[[Low-Rank Adapter]]"
aliases: [低秩适配器, Low-Rank Adapter]
---

# Low-Rank Adapter 中文条目

## 一句话直觉
低秩适配器是在大模型里插入小矩阵来学习增量更新，避免全量微调全部参数。

## 它为什么重要
它把 LLM 适配成本从“动全部参数”降到“只动少量低秩参数”，显著省显存和训练开销。

## 一个小例子
原本要更新一整块大矩阵，现在只训练两个小矩阵相乘得到近似更新，参数量可降一个数量级。

## 更正式的定义
将权重更新写作 \(\Delta W = BA\)，其中 \(A,B\) 的秩较小（\(r \ll d\)）。

## 数学形式（如有必要）
\[
\Delta W = BA
\]
- \(W\): 原始权重
- \(\Delta W\): 学到的增量
- \(r\): 低秩维度，控制表达能力与开销

## 核心要点
1. rank 是最关键的精度-效率旋钮。
2. 不同层最优 rank 往往不同。
3. 是 PEFT 方法族的核心构件。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 不固定统一 rank，而是搜索层间 rank 组合。

## 代表工作
- [[LLaMA-NAS]]: 通过 mixed-rank 设计提升压缩与性能权衡。

## 相关概念
- [[Parameter-Efficient Fine-Tuning]]
- [[Mixed-Rank Adapter]]
