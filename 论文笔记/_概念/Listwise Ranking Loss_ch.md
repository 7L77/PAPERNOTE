---
type: concept
language: zh-CN
source_concept_note: "[[Listwise Ranking Loss]]"
aliases: [Listwise Loss, Ranking List Optimization]
---

# Listwise Ranking Loss 中文条目

## 一句话直觉

Listwise Ranking Loss 把“整张排序列表”当作优化对象，而不只关心单点误差或样本对关系。

## 它为什么重要

NAS 实际上在做候选排序和筛选，listwise 目标通常更贴近最终使用场景。

## 一个小例子

两个方法在 pairwise 上都还可以，但 top-1 经常错位；listwise 目标会更直接惩罚这种整体次序偏差。

## 更正式的定义

代表性方法是 [[ListMLE]]，通过最大化真实排列在预测分数下的概率来训练模型。

## 数学形式（如有必要）

- 输入: 一组候选的预测分数。
- 目标: 与真实排序排列一致。
- 输出: 反映整表次序一致性的损失。

## 核心要点

1. 强调全局排序结构。
2. 与排序任务目标一致性高。
3. 常可与 weighted loss 做分阶段组合。

## 这篇论文里怎么用

- [[PWLNAS]]: 把 ListMLE 作为 listwise 代表，并在 NAS-Bench-101 上与 WARP 组合成分段策略。

## 代表工作

- [[PWLNAS]]: 系统比较 listwise、pairwise、weighted 三类损失。

## 相关概念

- [[ListMLE]]
- [[Pairwise Ranking Loss]]
