---
type: concept
language: zh-CN
source_concept_note: "[[Parameter-Efficient Fine-Tuning]]"
aliases: [参数高效微调, PEFT]
---

# Parameter-Efficient Fine-Tuning 中文条目

## 一句话直觉
PEFT 的核心是“尽量少训练参数也能适配新任务”，通常冻结大部分主干，只训练少量附加模块。

## 它为什么重要
在 LLM 场景，全量微调太贵；PEFT 让中小算力也能做任务定制。

## 一个小例子
几十亿参数模型里，只训练不到 1% 的 adapter 参数，就能获得可用任务性能。

## 更正式的定义
PEFT 是一类通过减少可训练参数和优化器状态开销来完成下游适配的方法集合。

## 核心要点
1. 目标是成本与效果的平衡。
2. adapter 结构与 rank 直接影响效果。
3. 可与 NAS 结合实现自动结构选择。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 把 PEFT 中的 adapter 配置问题转化为多目标 NAS。

## 代表工作
- [[LLaMA-NAS]]: 在 PEFT 框架下搜索更优 adapter 子网。

## 相关概念
- [[Low-Rank Adapter]]
- [[Neural Architecture Search]]
