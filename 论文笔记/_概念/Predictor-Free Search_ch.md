---
type: concept
language: zh-CN
source_concept_note: "[[Predictor-Free Search]]"
aliases: ["无预测器搜索", "免 surrogate 搜索"]
---

# Predictor-Free Search 中文条目

## 一句话直觉

Predictor-Free Search 就是搜索时不再训练单独的精度预测器，而是直接优化一个计算便宜的代理目标。

## 它为什么重要

很多 NAS 流程最耗时的是“构造子网-精度数据集 + 训练 predictor”。去掉这一步，后处理搜索可以从小时级降到分钟甚至秒级。

## 一个小例子

不用先评估上万子网去训练回归器，而是直接在结构 fitness 上跑 GA，就能在几十秒内拿到部署候选子网。

## 更正式的定义

Predictor-Free Search 指在部署搜索阶段不拟合显式 accuracy surrogate，而是直接用可计算目标（如零成本代理或结构评分）对架构做优化与排序。

## 核心要点

1. 优势是流程更快、更简单，工程链路更短。
2. 前提是代理信号与真实精度的排序相关性足够强。
3. 常与 MAC/参数/延迟等硬件约束联合使用。

## 这篇论文里怎么用

- [[DeepFedNAS]]: 直接最大化 \(F(A)\) 做部署搜索，报告显著的整体流程加速。

## 代表工作

- [[DeepFedNAS]]: 联邦 NAS 场景中的 predictor-free 部署搜索。
- [[Zero-Cost Proxy]]: 快速架构排序常用的代理信号家族。

## 相关概念

- [[Genetic Algorithm]]
- [[Zero-Cost Proxy]]
- [[Hardware-aware NAS]]

