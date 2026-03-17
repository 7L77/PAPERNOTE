---
type: concept
language: zh-CN
source_concept_note: "[[Partial Monitoring]]"
aliases: [部分监控, 部分反馈决策]
---

# Partial Monitoring 中文条目

## 一句话直觉

Partial Monitoring 指的是：你每轮只能拿到“部分反馈”，看不到完整奖励，但仍要不断做决策并学到更优策略。

## 它为什么重要

很多真实问题都不是“选了动作就拿到完整真值”，而是只能看到间接信号。理论上需要专门处理这种反馈缺口。

## 一个小例子

像广告投放中你只能看到已展示广告的点击反馈，看不到所有广告在同一时刻的真实偏好排序，只能靠部分反馈逐步学习。

## 更正式的定义

学习者在每轮中：
1. 选择动作；
2. 接收观测反馈；
3. 承担奖励/损失，但奖励不是完全可见。

目标是最小化累计 regret。

## 数学形式（如有必要）

常见 regret 形式：
\[
\mathrm{Reg}_t=\sum_{\tau=1}^{t}\left(r(a^*)-r(a_\tau)\right)
\]
其中 \(a^*\) 是最优固定动作，\(r(\cdot)\) 是期望奖励。在 partial monitoring 中，需要借助观测去间接估计奖励差异。

## 核心要点

1. 反馈强度弱于全信息场景。
2. 可观测性条件决定是否能高效学习。
3. 很适合分析“只看到间接代理信号”的序列决策过程。

## 这篇论文里怎么用
- [[RoBoT]]: 把权重向量搜索过程放进 partial monitoring 框架，并据此推导期望排名上界。

## 代表工作

- [[RoBoT]]: 在训练免费 NAS 中使用 partial monitoring 视角做理论分析。

## 相关概念

- [[Bayesian Optimization]]
- [[Information Directed Sampling]]
