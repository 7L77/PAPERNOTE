---
type: concept
language: zh-CN
source_concept_note: "[[Pearson Correlation Coefficient]]"
aliases: [皮尔逊相关系数, Pearson相关]
---

# Pearson Correlation Coefficient 中文条目

## 一句话直觉
Pearson 相关衡量的是“两个向量去均值、归一化后是否同向变化”，比直接点积更不怕尺度变化。

## 为什么重要
结构化剪枝会改变梯度/激活幅值；这时用 Pearson 可以更稳地比较方向一致性，而不是被数值大小误导。

## 小例子
若 `y = 3x + 5`，点积会因比例变化而改变很多，但 Pearson 相关仍接近 1。

## 定义
对变量 `x` 与 `y`：
\[
\rho(x,y)=\frac{\mathrm{cov}(x,y)}{\sigma_x \sigma_y}
\]
取值范围 `[-1,1]`，`1` 表示完全正线性相关，`-1` 表示完全负线性相关。

## 核心要点
1. 先中心化再按方差归一化。
2. 对仿射缩放（`ax+b`）具有不变性（符号受 `a` 影响）。
3. 它反映线性方向一致性，不代表因果关系。

## 在本文中的作用
- [[TraceNAS]] 用它计算基座模型与候选子网的分层梯度轨迹相关，再做稀疏度加权聚合。

## 代表工作
- [[TraceNAS]]: 将 Pearson 作为 zero-shot 剪枝代理的核心算子。

## 相关概念
- [[Spearman's Rank Correlation]]
- [[Gradient Trace Correlation]]
- [[Gradient Alignment]]
