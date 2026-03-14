---
type: concept
language: zh-CN
source_concept_note: "[[Fisher Information Matrix]]"
aliases: [费舍尔信息矩阵, FIM]
---

# Fisher Information Matrix 中文条目

## 一句话直觉

Fisher Information Matrix（FIM）描述了“参数轻微变化会让模型预测分布变化多大”，变化越敏感，说明该方向包含的信息越多。

## 它为什么重要

FIM 能把“参数可估计性/不确定性”变成可计算对象，是连接统计估计理论与深度网络训练行为的核心工具。

## 一个小例子

如果两个参数方向里，一个方向改一点几乎不影响输出，另一个方向改一点输出就变化很大，那么后者对应更高的信息量，FIM 会体现这种差异。

## 更正式的定义

对分布 `p_theta(y|x)`，FIM 是 score 向量外积的期望：

`F(theta) = E[grad_theta log p_theta(y|x) * grad_theta log p_theta(y|x)^T]`。

## 数学形式（如有必要）

VKDNW 文中写法（Sec. II-A, Eq. (2)）为：

`F(theta) = E[grad_theta sigma_theta(c|x) grad_theta sigma_theta(c|x)^T]`。

其中 `theta` 为网络参数，`x` 为输入，`c` 为类别变量。

## 核心要点

1. FIM 是半正定矩阵，谱结构有明确含义。
2. FIM 的逆与 [[Cramer-Rao Bound]] 中估计方差下界相关。
3. FIM 谱可用于构建训练前 proxy（如 VKDNW）。

## 这篇论文里怎么用

- [[VKDNW]]: 用代表性特征值谱熵构造零训练 NAS 排序分数。

## 代表工作

- [[VKDNW]]: 将 FIM 谱信息用于 training-free NAS。

## 相关概念

- [[Cramer-Rao Bound]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
