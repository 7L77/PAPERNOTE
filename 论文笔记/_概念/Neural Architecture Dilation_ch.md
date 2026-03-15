---
type: concept
language: zh-CN
source_concept_note: "[[Neural Architecture Dilation]]"
aliases: [神经架构扩张, Neural Architecture Dilation]
---

# Neural Architecture Dilation 中文条目

## 一句话直觉

Neural Architecture Dilation（神经架构扩张）就是保留原本已经很强的 backbone，不推倒重来，而是在旁路加一条可学习/可搜索的“扩张分支”来补鲁棒性或能力。

## 它为什么重要

很多鲁棒 NAS 方法要整网重搜，代价高且容易损伤标准精度。架构扩张提供了折中路径：让 backbone 继续负责干净样本表现，让增量分支重点补对抗鲁棒性。

## 一个小例子

例如 CIFAR-10 上某个 WRN backbone 在干净样本上很好，但遇到 PGD 攻击明显掉点。  
用架构扩张后，每个 stage 旁边挂一个 cell，输出做相加融合。这样主干语义保留，同时新增分支专门学习更稳健的特征。

## 更正式的定义

神经架构扩张是把基础模型 `f_b` 扩展成 `f_hyb = f_b + f_d` 的策略，其中 `f_d` 是按 block/stage 挂接的增量结构，常在“标准性能约束 + 计算预算约束”下优化，以减少鲁棒性提升带来的副作用。

## 数学形式（如有必要）

在 NADAR 中，典型形式为：

`z_hyb^(l) = f_b^(l)(z_hyb^(l-1)) + f_d^(l)(z_hyb^(l-1), z_hyb^(l-2))`

- `f_b^(l)`: backbone 的第 `l` 个 block
- `f_d^(l)`: 对应的 dilation cell
- `z_hyb^(l)`: 融合后的特征

该式体现“加法扩张”而不是“替换主干”。

## 核心要点

1. 它是增量式设计，不是从零重搜整网。
2. 适合“要鲁棒性也要尽量保标准精度”的场景。
3. 若没有标准约束/FLOPs 约束，扩张分支可能带来不稳定 trade-off。

## 这篇论文里怎么用

- [[NADAR]]: 为每个 backbone block 附加 NAS cell，并在对抗目标下联合标准约束与 FLOPs 约束进行优化。

## 代表工作

- [[NADAR]]: 将 Neural Architecture Dilation 系统化用于对抗鲁棒性优化。

## 相关概念

- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Adversarial Robustness]]
