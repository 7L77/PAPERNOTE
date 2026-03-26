---
type: concept
language: zh-CN
source_concept_note: "[[Universal Adversarial Perturbation]]"
aliases: [通用对抗扰动, UAP]
---

# Universal Adversarial Perturbation 中文条目

## 一句话直觉

UAP（Universal Adversarial Perturbation）是“一个共享扰动向量”，可以同时让很多样本被模型误判，而不是每个样本单独求一个扰动。

## 它为什么重要

在鲁棒 NAS 场景里，UAP 可以快速构造统一的对抗评估空间，减少对每个候选结构逐样本攻击生成的成本。

## 一个小例子

如果有 1 万张图，传统做法要为每张图单独生成攻击；UAP 做法是先学到一个 \(v\)，然后统一用 \(x_i+v\) 做评估。

## 更正式的定义

给定数据集 \(D_S=\{(x_i,y_i)\}\)，寻找一个统一扰动 \(v\)，使得对多数样本有：

\[
\mathcal{C}(x_i+v)\neq y_i,\quad \|v\|_p\le\epsilon
\]

## 核心要点

1. UAP 是样本无关扰动（sample-agnostic）。
2. UAP 的跨架构迁移性决定其在 NAS 中的实用价值。
3. fooling ratio 高不一定代表用于搜索时最优。

## 这篇论文里怎么用

- [[RTP-NAS]]: 用 UAP 构造 [[Adversarial Input Space]]，再在该空间上做无训练剪枝评分。

## 代表工作

- [[RTP-NAS]]: 将 UAP 用于鲁棒 training-free NAS。

## 相关概念

- [[Adversarial Input Space]]
- [[FGSM]]
- [[PGD Attack]]
- [[Adversarial Robustness]]
