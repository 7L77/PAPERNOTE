---
type: concept
language: zh-CN
source_concept_note: "[[One-Epoch Proxy Evaluation]]"
aliases: [单轮代理评估, One-Epoch Proxy]
---

# One-Epoch Proxy Evaluation 中文条目

## 一句话直觉
不把每个候选都完整训练到底，而是统一只训 1 个 epoch，用早期精度做快速排序信号。

## 它为什么重要
NAS 的瓶颈是评估开销。1-epoch 代理能显著降低单候选成本，让迭代次数大幅提高。

## 一个小例子
在同样训练设置下，A 架构 1-epoch 达到 62%，B 只有 51%，则优先把算力投给 A。

## 更正式的定义
在固定训练协议下，对候选架构只训练一个 epoch，并以此时的验证/测试准确率作为架构质量估计。

## 核心要点
1. 它主要服务“排序”，不是最终收敛性能结论。
2. 必须控制训练协议一致，否则可比性会下降。
3. 适合需要高吞吐候选评估的迭代搜索。

## 这篇论文里怎么用
- [[Iterative LLM-Based NAS with Feedback Memory]]: 每轮候选都用 one-epoch Top-1 精度作为反馈，驱动下一轮提示改进。

## 代表工作
- [[Iterative LLM-Based NAS with Feedback Memory]]: 在 CIFAR-10/100 与 ImageNette 上使用该代理信号完成大规模迭代搜索。

## 相关概念
- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Spearman's Rank Correlation]]
