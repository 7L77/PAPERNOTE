---
type: concept
language: zh-CN
source_concept_note: "[[Pareto-Guided Supernet Training]]"
aliases: ["Pareto 路径引导训练", "Pareto 缓存引导 supernet 训练"]
---

# Pareto-Guided Supernet Training 中文条目

## 一句话直觉

与其在 supernet 训练里随机抽子网，不如先找一批 Pareto 意义上更优的子网缓存，再用它们做有结构的训练课程。

## 它为什么重要

超大搜索空间里随机子网大多质量一般，会给共享权重带来噪声更新；路径引导训练能让梯度信号更稳定、更有效。

## 一个小例子

如果我们先离线得到覆盖低到高 MAC 档位的 60 个高质量子网，再在联邦轮次中优先从这批子网采样，通常比完全随机采样训练效果更好。

## 更正式的定义

Pareto-Guided Supernet Training 是一种 curriculum 策略：先离线构建近 Pareto 最优子网集合，再在权重共享 supernet 训练中用该集合指导子网分配与采样。

## 核心要点

1. 把子网采样从“无引导随机”变成“结构化课程学习”。
2. 通常能提升共享权重质量，进而提升后处理搜索效果。
3. 通过多预算缓存可同时覆盖不同资源档位。

## 这篇论文里怎么用

- [[DeepFedNAS]]: 先生成 60 子网 Pareto cache，再在联邦训练里执行边界子网 + cache 抽样策略。

## 代表工作

- [[DeepFedNAS]]: 在联邦场景下系统化实现 Pareto 引导训练。
- [[SuperFedNAS]]: 随机采样基线，被该策略显著改进。

## 相关概念

- [[Pareto Front]]
- [[Super-network]]
- [[Federated Neural Architecture Search]]

