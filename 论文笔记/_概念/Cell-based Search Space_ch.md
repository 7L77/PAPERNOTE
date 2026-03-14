---
type: concept
language: zh-CN
source_concept_note: "[[Cell-based Search Space]]"
aliases: [Cell 搜索空间, 基于 Cell 的 NAS 空间]
---

# Cell-based Search Space 中文条目

## 一句话直觉
先搜一个小 cell，再把它重复堆叠成大网络，而不是直接搜索整网。

## 它为什么重要
这样能明显缩小搜索难度，并让搜索到的 cell 更容易迁移到不同数据集和任务设置。

## 一个小例子
把一个 cell 看成 DAG，边上可选 3x3 conv、1x1 conv、skip 等操作；搜索完成后把该 cell 重复堆叠得到最终网络。

## 更正式的定义
Cell-based 搜索空间把候选架构参数化为一个或少量 cell 图的微结构，宏观堆叠深度通常固定或单独设置。

## 核心要点
1. 重点搜索微结构拓扑与边操作类型。
2. 最终模型由重复堆叠 cell 构造。
3. 是 DARTS 与多种 NAS benchmark 的常见范式。

## 这篇论文里怎么用
- [[SWAP-NAS]]: 在 DARTS 风格 cell 编码上做进化搜索，并用 SWAP 分数评估候选。

## 代表工作
- [[SWAP-NAS]]: 将 regularized SWAP 指标接入 cell-based 进化搜索。

## 相关概念
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]

