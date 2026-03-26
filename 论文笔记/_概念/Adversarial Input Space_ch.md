---
type: concept
language: zh-CN
source_concept_note: "[[Adversarial Input Space]]"
aliases: [对抗输入空间, 扰动输入空间]
---

# Adversarial Input Space 中文条目

## 一句话直觉

对抗输入空间就是把干净样本替换成受扰动样本后形成的评估空间，用来更早衡量模型在攻击条件下的表现。

## 它为什么重要

如果搜索只看 clean 数据，得到的架构未必鲁棒；在对抗输入空间上打分，可以让搜索目标更贴近鲁棒性。

## 一个小例子

从 \(\{(x_i,y_i)\}\) 出发，构造 \(\{(x_i+\delta_i,y_i)\}\)（逐样本攻击）或 \(\{(x_i+v,y_i)\}\)（UAP 共享扰动）。

## 更正式的定义

对抗输入空间 \(D_A\) 指在给定扰动约束下，由对抗扰动样本组成的输入集合。

## 核心要点

1. 构造方式决定可迁移性与计算成本。
2. 在 NAS 中，空间可迁移性决定不同架构评分是否可比。
3. 攻击强度越大通常越能反映鲁棒差异，但构造成本也会增加。

## 这篇论文里怎么用

- [[RTP-NAS]]: 使用 UAP 构造 \(D_A=\{(x_i+v,y_i)\}\)，并在该空间计算对抗 NTK 条件数与线性区域数。

## 代表工作

- [[RTP-NAS]]: 用对抗输入空间驱动 training-free robust NAS 剪枝。

## 相关概念

- [[Universal Adversarial Perturbation]]
- [[Adversarial Robustness]]
- [[FGSM]]
- [[PGD Attack]]
