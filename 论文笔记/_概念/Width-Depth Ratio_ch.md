---
type: concept
language: zh-CN
source_concept_note: "[[Width-Depth Ratio]]"
aliases: [宽深比, WD Ratio]
---

# Width-Depth Ratio 中文条目

## 一句话直觉
`Width-Depth Ratio`（宽深比）衡量的是一个分阶段 CNN 把容量更偏向“加宽”还是“加深”。

## 它为什么重要
在相同参数量附近，宽深分配不同会导致不同的鲁棒性表现；所以仅看参数量不够。

## 一个小例子
两个模型都是约 26M 参数，一个宽而浅、一个窄而深，PGD/AA 下鲁棒精度可能明显不同。

## 更正式的定义

$$
\text{WD ratio}=\frac{1}{n-1}\sum_{i=1}^{n-1}\frac{W_i}{D_i}
$$

`W_i` 是第 `i` 个 stage 的宽度，`D_i` 是该 stage 的深度，通常排除最后一个 stage。

## 核心要点
1. 它描述的是结构分配方式，不是参数总量。
2. 便于跨不同 stage 设计比较。
3. 可作为鲁棒架构筛选指标。

## 这篇论文里怎么用
- [[Robust Principles]]: 用 WD 比率找到了鲁棒区间 `[7.5, 13.5]`。

## 代表工作
- [[Robust Principles]]: 系统提出并实证 WD 比率在鲁棒设计中的作用。

## 相关概念
- [[Lipschitz Constant]]
- [[Adversarial Robustness]]

