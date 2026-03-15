---
type: concept
language: zh-CN
source_concept_note: "[[Super-network]]"
aliases: [超网络, Super-network]
---

# Super-network 中文条目

## 一句话直觉
Super-network 是把大量候选结构装进一个大网络里共享训练，再从中导出子网。

## 它为什么重要
它把 NAS 从“每个候选都重训一次”的高成本流程，变成“训练一次后批量筛选”的可行流程。

## 一个小例子
某层有多个候选算子，超网会把这些分支统一管理，最后按搜索结果导出具体路径作为部署模型。

## 更正式的定义
Super-network 是对候选架构空间的统一参数化表示，借助权重共享支持 one-shot 架构搜索。

## 核心要点
1. one-shot NAS 的基础设施。
2. 通过权重共享节省搜索成本。
3. 部署前需要导出并固化子网结构。

## 这篇论文里怎么用
- [[LLaMA-NAS]]: 以 mixed-rank adapter 组建超网，再进行多目标搜索。

## 代表工作
- [[LLaMA-NAS]]: 使用超网来摊销 LLM adapter 搜索成本。

## 相关概念
- [[One-shot NAS]]
- [[Mixed-Rank Adapter]]
