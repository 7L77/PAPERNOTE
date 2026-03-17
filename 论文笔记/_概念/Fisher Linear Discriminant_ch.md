---
type: concept
language: zh-CN
source_concept_note: "[[Fisher Linear Discriminant]]"
aliases: [FLD, Fisher 线性判别]
---

# Fisher Linear Discriminant 中文条目

## 一句话直觉
Fisher 线性判别的目标是“类间尽量分开、类内尽量紧凑”。

## 它为什么重要
它提供了“分离度 / 方差”平衡思想，常用于构造稳健统计指标。

## 一个小例子
两类样本均值差不大但方差很大时，判别分数不会虚高；均值差大且方差小时分数更高。

## 更正式的定义
经典形式通过最大化
\[
J(w)=\frac{w^T S_B w}{w^T S_W w}
\]
其中 `S_B` 是类间散度，`S_W` 是类内散度。

## 核心要点
1. 体现“分离信号与噪声”比值思想。
2. 广泛用于判别分析与特征提取。
3. 很多现代启发式都可看作这一思想的变体。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 的 HDA 受 FLD 启发。
- 其候选 gamma 公式本质上是“均值差 / 方差和”的比例结构。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[Hyperparameter Detection Algorithm]]
- [[Radial Basis Function Kernel]]

