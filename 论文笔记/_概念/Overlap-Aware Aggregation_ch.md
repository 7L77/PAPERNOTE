---
type: concept
language: zh-CN
source_concept_note: "[[Overlap-Aware Aggregation]]"
aliases: ["重叠感知聚合", "掩码感知聚合"]
---

# Overlap-Aware Aggregation 中文条目

## 一句话直觉

在 supernet 联邦训练里，不同客户端只会更新自己子网激活到的参数；Overlap-Aware Aggregation 只对“真的被更新过”的参数做平均。

## 它为什么重要

如果把所有客户端都一视同仁平均，会把很多未激活参数当成“零更新”稀释掉，导致共享权重更新失真。

## 一个小例子

某轮中 8 个客户端里只有 2 个子网包含参数 \(\theta_i\)，那 \(\theta_i\) 应该按这 2 个有效更新聚合，而不是除以 8。

## 更正式的定义

Overlap-Aware Aggregation 是一种带参数激活掩码的联邦聚合规则：按每个参数在各客户端子网中的实际重叠/激活情况进行归一化更新。

## 数学形式（如有必要）

记 \(I_k(\theta)\in\{0,1\}\) 表示客户端 \(k\) 的子网是否激活参数 \(\theta\)。聚合时用掩码加权归一化，而不是固定按客户端总数平均。

## 核心要点

1. 对权重共享 supernet 的稀疏更新非常关键。
2. 能避免“未激活参数被错误平均”。
3. 在子网差异较大时可显著提升训练稳定性。

## 这篇论文里怎么用

- [[DeepFedNAS]]: 在 Eq. (2) 与 Algorithm 1 中使用二值掩码的 overlap-aware MaxNet 聚合。

## 代表工作

- [[DeepFedNAS]]: 在 Pareto 引导联邦 supernet 训练中明确实现此机制。
- [[SuperFedNAS]]: 联邦 supernet 聚合范式的重要基线。

## 相关概念

- [[Super-network]]
- [[Parameter Sharing in NAS]]
- [[Federated Neural Architecture Search]]

