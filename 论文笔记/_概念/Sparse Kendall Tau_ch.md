---
type: concept
language: zh-CN
source_concept_note: "[[Sparse Kendall Tau]]"
aliases: [稀疏 Kendall Tau, sKT]
---

# Sparse Kendall Tau 中文条目

## 一句话直觉

Sparse Kendall Tau 是对 Kendall 排序相关性的“降噪版”：把非常接近的分数先做精度量化，再评估排序一致性，避免把微小噪声当成严重排序错误。

## 它为什么重要

NAS 里很多候选架构性能非常接近。若直接用标准 Kendall's Tau，极小的预测波动也会被记成“顺序翻转”，会高估模型的排序失误。

## 一个小例子

两个架构预测精度分别是 97.23% 和 97.25%。如果量化精度设为 0.1%，它们都会映射到 97.2%，不再因为这点差异被当作错误交换。

## 更正式的定义

Sparse Kendall Tau（sKT）先按固定精度阈值对预测值离散化（NAS-Bench-301 中使用 0.1% 精度），再计算 Kendall's Tau，从而降低对小幅噪声排序翻转的敏感性。

## 数学形式（如有必要）

先做量化：

y_hat' = round(y_hat / delta) * delta

再在 y_hat' 与 y_true 上计算 Kendall's Tau。

- delta：量化精度阈值（例如 0.1%）。

## 核心要点

1. 比原始 Kendall's Tau 更抗噪声。
2. 更贴近“实际可用”的排序质量评估。
3. 仍能识别明显的排序错误。

## 这篇论文里怎么用

- [[NAS-Bench-301]]: 用 sKT + R2 共同评估 surrogate 的拟合质量和留一优化器外推能力。

## 代表工作

- [[NAS-Bench-301]]: 在 surrogate benchmark 评估中系统使用 sKT。
- [[Kendall's Tau]]: sKT 所基于的原始秩相关指标。

## 相关概念

- [[Kendall's Tau]]
- [[Surrogate Predictor]]
- [[Surrogate NAS Benchmark]]

