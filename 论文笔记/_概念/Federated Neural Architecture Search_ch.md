---
type: concept
language: zh-CN
source_concept_note: "[[Federated Neural Architecture Search]]"
aliases: ["联邦神经架构搜索", "FedNAS"]
---

# Federated Neural Architecture Search 中文条目

## 一句话直觉

Federated Neural Architecture Search（FedNAS）就是把“找网络结构”这件事也放到联邦学习里做，而不是先在中心端拍脑袋定好结构再去联邦训练。

## 它为什么重要

联邦场景里客户端数据分布和硬件能力差异都很大，单一手工结构通常不够好；FedNAS 可以在通信与设备约束下自动找到更合适的结构。

## 一个小例子

手机输入法场景中，低端设备需要更小子网，高端设备可用更大子网。FedNAS 可在同一 supernet 下搜索并分配更匹配的架构。

## 更正式的定义

FedNAS 研究如何在数据去中心化、通信受限、客户端异构显著的联邦环境中进行神经架构搜索与优化。

## 核心要点

1. 不再把架构当固定前提，而是与联邦优化联合设计。
2. 同时处理统计异构（non-IID）与系统异构（算力/内存/延迟）。
3. 常借助 supernet 与权重共享降低搜索成本。

## 这篇论文里怎么用

- [[DeepFedNAS]]: 用 Pareto 引导的 supernet 训练和 predictor-free 部署搜索，完整实现 FedNAS 闭环。

## 代表工作

- [[DeepFedNAS]]: predictor-free + hardware-aware 的联邦 NAS。
- [[SuperFedNAS]]: 解耦 supernet 训练与后处理搜索的经典框架。

## 相关概念

- [[Neural Architecture Search]]
- [[Super-network]]
- [[Hardware-aware NAS]]

