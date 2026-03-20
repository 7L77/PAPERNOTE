---
type: concept
language: zh-CN
source_concept_note: "[[Entropy]]"
aliases: [信息熵, Entropy]
---

# Entropy 中文条目

## 一句话直觉
Entropy（信息熵）衡量不确定性，分布越“平均”、越难预测，熵通常越大。

## 它为什么重要
它是信息论最基础的量之一，常用于不确定性分析、正则化和 proxy 设计。

## 一个小例子
公平硬币（正反各 50%）比 99% 都是正面的硬币熵更高，因为前者更不确定。

## 更正式的定义
离散分布 `p` 的 Shannon 熵定义为 `H(p) = -sum_i p_i log p_i`。

## 数学形式（如有必要）
当 `K` 类概率完全均匀时，熵达到最大值 `log K`。

## 核心要点
1. 熵描述不确定性，不直接等价于“好坏”。
2. 它依赖整个概率分布形状。
3. 在 IB、校准和 zero-cost proxy 中都很常见。

## 这篇论文里怎么用
- [[IBFS]]: 用 Jacobian 谱分布的熵作为架构表达性打分。

## 代表工作
- Shannon (1948): 信息熵基础定义。
- [[IBFS]]: 熵驱动的训练自由 NAS 排序。

## 相关概念
- [[Information Bottleneck]]
- [[KL Divergence]]
- [[Zero-Cost Proxy]]
