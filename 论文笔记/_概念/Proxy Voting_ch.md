---
type: concept
language: zh-CN
source_concept_note: "[[Proxy Voting]]"
aliases: [代理投票, Voting Proxy]
---

# Proxy Voting 中文条目

## 一句话直觉

`Proxy Voting` 就是让多个 proxy 一起“表决”架构好坏，减少单个 proxy 偏差导致的误判。

## 它为什么重要

zero-shot NAS 的代理分数对数据、初始化、搜索空间很敏感，多代理融合通常更稳健。

## 一个小例子

三个 proxy 中有两个认为架构 A 比 B 好，另一个相反，则多数票结果选 A，从而抑制单代理噪声。

## 更正式的定义

Proxy voting 指通过多数票、排名聚合或学习型融合，把多个代理信号合成为一个最终排序策略。

## 数学形式（如有必要）

常见聚合方式：

- 多数投票（majority voting）
- rank-sum / rank-product
- 学习型融合器（如随机森林）

## 核心要点

1. 核心价值在于稳健性提升。
2. 代理间互补性越强，融合价值越高。
3. 代价是工程复杂度和计算开销增加。

## 这篇论文里怎么用

- [[WRCor]]: 提出 SPW 与 SJW 两种投票代理，在多个设置下提升排序稳定性和搜索结果。

## 代表工作

- [[WRCor]]: 将 WRCor 与 SynFlow/JacCor/PNorm 组合进行投票。
- [[ZCP-Eval]]: 从评估角度说明单代理在跨设置下不稳定，支持投票思路。

## 相关概念

- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Non-linear Ranking Aggregation]]


