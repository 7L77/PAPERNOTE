---
type: concept
language: zh-CN
source_concept_note: "[[Functional Inheritance]]"
aliases: [功能继承, 功能保持性]
---

# Functional Inheritance 中文条目

## 一句话直觉
剪枝后的模型如果还能沿着原预训练模型的“功能轨道”优化，就更容易用较少训练恢复性能。

## 为什么重要
LLM 压缩通常离不开后续恢复训练，先筛出“继承性更强”的结构，能显著降低恢复成本并提高最终上限。

## 小例子
两个同参数量的剪枝模型里，和基座梯度方向更一致的那个，往往在同等 CPT token 下恢复得更快更好。

## 定义
Functional Inheritance 指压缩/剪枝模型对预训练模型功能状态的保留程度，体现为有限再训练条件下的可恢复性。

## 核心要点
1. 它关注的是“恢复潜力”，不只看剪枝后瞬时精度。
2. 由全局结构依赖决定，不能只靠局部权重打分。
3. 可用 zero-shot 代理（如梯度轨迹对齐）近似衡量。

## 在本文中的作用
- [[TraceNAS]] 把功能继承作为核心目标，使用 `Phi` 对候选架构进行排序。

## 代表工作
- [[TraceNAS]]: 通过梯度轨迹对齐实现面向继承性的训练自由搜索。

## 相关概念
- [[Gradient Trace Correlation]]
- [[Training-free NAS]]
- [[Structured Pruning]]
