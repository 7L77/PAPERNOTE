---
type: concept
language: zh-CN
source_concept_note: "[[TRADES]]"
aliases: [TRADES, 对抗训练精度鲁棒折中]
---

# TRADES 中文条目

## 一句话直觉

TRADES 通过“干净样本分类损失 + 干净/对抗预测一致性损失”来平衡精度和鲁棒性。

## 它为什么重要

只追求对抗鲁棒往往会明显掉 clean 精度，TRADES 给了更可控的折中目标。

## 一个小例子

模型既要在原图上分类正确，也要在对抗样本上保持与原图预测分布接近。

## 更正式的定义

在有界扰动集合内，对 clean CE 和 clean-vs-adv KL 一起优化。

## 数学形式（如有必要）

`L = CE(f(x), y) + beta * KL(f(x) || f(x_adv))`。

## 核心要点

1. `beta` 控制鲁棒-精度权衡。
2. 是常见强基线鲁棒训练目标。
3. 可用于 NAS 搜索后的最终重训练。

## 这篇论文里怎么用
- [[RNAS-CL]]: 在搜索结束后，替换训练阶段目标做 TRADES 重训，提升 PGD 等攻击下表现。

## 代表工作

- Zhang et al. (2019): TRADES 原论文。

## 相关概念

- [[Adversarial Robustness]]
- [[PGD Attack]]
