---
type: concept
language: zh-CN
source_concept_note: "[[Pareto Front]]"
aliases: [帕累托前沿, Pareto Front]
---

# Pareto Front 中文条目

## 一句话直觉
Pareto Front 是“最优权衡边界”：你想在某个目标上再变好，就要在另一个目标上付出代价。

## 它为什么重要
在模型压缩里，我们通常不只追求精度，还关心参数量和延迟。Pareto 前沿可以给出一组可部署选择。

## 一个小例子
若 A 比 B 更准但更大，两者都可能在前沿上；只有当某模型“又更小又更准”时，另一模型才会被淘汰。

## 更正式的定义
若不存在另一个可行解在至少一个目标上更优且在其他目标不差，则该解是 Pareto 最优解。

## 核心要点
1. 关注权衡，不是单一排名。
2. 前沿形状取决于目标定义。
3. 多目标 NAS 的自然输出就是 Pareto 解集。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 以“任务性能 + adapter 参数量”构建 Pareto 候选并据预算选型。

## 代表工作
- [[LLaMA-NAS]]: 将 Pareto 视角用于 LLM adapter 结构搜索。

## 相关概念
- [[NSGA-II]]
- [[Neural Architecture Search]]
