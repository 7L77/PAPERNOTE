---
type: concept
language: zh-CN
source_concept_note: "[[Zero-Cost Proxy]]"
aliases: [零训练代理, ZCP]
---

# Zero-Cost Proxy 中文条目

## 一句话直觉
Zero-Cost Proxy（ZCP）是在几乎不训练网络的情况下，用很便宜的统计量去预估架构潜力。

## 它为什么重要
NAS 里真正昂贵的是“把每个候选都完整训练一遍”。ZCP 可以先做低成本粗筛。

## 一个小例子
两个候选架构都还没训练时，若 A 的 `jacov` 显著高于 B，就优先把计算资源给 A。

## 更正式的定义
ZCP 是在初始化阶段从网络结构或极少量前后向信息提取出的分数/特征，用作性能预测的代理输入。

## 核心要点
1. 计算便宜、适合大规模搜索预筛。
2. 对 clean 与 robust 目标的有效性可能不同。
3. 多个 ZCP 组合通常比单一 ZCP 更稳。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 将 15 种 ZCP 作为随机森林输入，预测 clean/robust 准确率。

## 代表工作
- [[ZCP-Eval]]: 面向鲁棒目标的系统评测。
- [[NAS-Bench-Suite-Zero]]: ZCP 的基准化比较。

## 相关概念
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
- [[Robust Neural Architecture Search]]


## 补充（2026-03-14）
- [[AZ-NAS]]: 该论文把多种 zero-cost proxy 组合用于 training-free NAS 排名。
