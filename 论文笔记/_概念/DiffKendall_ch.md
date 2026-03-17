---
type: concept
language: zh-CN
source_concept_note: "[[DiffKendall]]"
aliases: [可微 Kendall Tau, DiffKendall]
---

# DiffKendall 中文条目

## 一句话直觉
DiffKendall 是把 Kendall Tau 变成“可导版本”的排序指标，这样模型能直接学“排对顺序”。

## 它为什么重要
原始 Kendall Tau 依赖符号函数，不可导；DiffKendall 让排序目标可以直接进入反向传播。

## 一个小例子
若真实顺序是 A>B，DiffKendall 会给“分差方向正确”的预测连续奖励，而不是只有对/错二值反馈。

## 更正式的定义
它用 sigmoid 近似符号比较，再在所有样本对上累积一致性，得到可微的 Kendall 近似值。

## 数学形式（如有必要）
\[
\tau_d = \frac{1}{\binom{L}{2}}\sum_{i\neq j}\sigma_\alpha(\Delta x_{ij})\sigma_\alpha(\Delta y_{ij})
\]
其中 \(\sigma_\alpha\) 为平滑符号近似。

## 核心要点
1. 面向“排序”而不是“点估计误差”。
2. 兼容梯度优化。
3. 需要调节平滑系数 alpha。

## 这篇论文里怎么用
- [[ParZC]]: 作为核心损失函数提升 KD/SP 排序相关性。

## 代表工作
- [[ParZC]]: 在 NAS 排序任务中验证了该损失有效性。

## 相关概念
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
- [[Zero-Cost Proxy]]
