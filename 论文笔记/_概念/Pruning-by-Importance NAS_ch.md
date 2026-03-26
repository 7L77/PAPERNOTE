---
type: concept
language: zh-CN
source_concept_note: "[[Pruning-by-Importance NAS]]"
aliases: [重要性剪枝NAS, Pruning-by-Importance NAS]
---

# Pruning-by-Importance NAS 中文条目

## 一句话直觉
它不是一次次“训练完整候选架构”去比优劣，而是每轮都问“这条边上哪个算子当前最不重要”，然后把它剪掉。

## 它为什么重要
这样可以把原本组合爆炸的 NAS 问题，转成一系列局部删减决策，通常能显著降低搜索成本。

## 一个小例子
某条边有 5 个算子。如果删除算子 A 后可训练性变好、表达性下降又很小，那么 A 的重要性就低，会优先被剪掉。

## 更正式的定义
Pruning-by-importance NAS 指从超网出发，依据代理指标估计每个候选算子的“重要性”，并在迭代中持续删除低重要性算子的 NAS 策略。

## 数学形式（如有必要）
常见写法是多指标排名求和：

$$
s(o_j) = s_1(o_j) + s_2(o_j)
$$

其中 `s_1`、`s_2` 是不同代理信号下的排序名次（如可训练性、表达性）。`s(o_j)` 越低，越可能被剪。

## 核心要点
1. 通过逐轮删减来收缩搜索空间。
2. 结果高度依赖代理指标质量。
3. 很适合用 rank 聚合融合多个代理信号。

## 这篇论文里怎么用
- [[TE-NAS]]: 对“删除某算子后”的 NTK 与线性区域变化分别排序，再做边级剪枝。

## 代表工作
- [[TE-NAS]]: 训练自由 rank-pruning NAS 的经典示例。

## 相关概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
