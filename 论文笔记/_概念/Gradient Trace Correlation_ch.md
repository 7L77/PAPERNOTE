---
type: concept
language: zh-CN
source_concept_note: "[[Gradient Trace Correlation]]"
aliases: [梯度轨迹相关性, 梯度轨迹对齐]
---

# Gradient Trace Correlation 中文条目

## 一句话直觉
如果剪枝后模型在同一批数据上的梯度方向仍和基座模型接近，它通常更容易恢复到高性能状态。

## 为什么重要
在预训练模型剪枝里，我们更关心“功能是否继承”而不是“从零是否好训”；梯度轨迹相关性能直接刻画这种继承性。

## 小例子
对基座与候选模型在小校准集上求梯度，分层做标准化后计算 Pearson 相关；相关越高，说明候选越贴近原优化流形。

## 定义
Gradient Trace Correlation 指在同一数据分布下，比较两个模型（常见是基座与剪枝候选）聚合梯度轨迹方向一致性的度量。

## 数学形式（如有必要）
\[
g = \mathbb{E}_{b \in B}[\nabla_\theta \mathcal{L}(M(b;\theta))]
\]
\[
\rho^{(l)}=\mathrm{Pearson}\left(g_{sub}^{(l)}, g_{base}^{(l)}\right)
\]
实践中常在层间进一步加权聚合为全局分数。

## 核心要点
1. 它关注方向而非绝对幅值。
2. Pearson 标准化可以缓解剪枝导致的尺度偏移。
3. 可直接作为 zero-shot 架构排序代理。

## 在本文中的作用
- [[TraceNAS]] 将分层梯度轨迹相关按稀疏度加权，形成核心 proxy `Phi`。

## 代表工作
- [[TraceNAS]]: 在 LLM 结构化剪枝搜索中系统化使用该代理。

## 相关概念
- [[Gradient Alignment]]
- [[Pearson Correlation Coefficient]]
- [[Training-free NAS]]
