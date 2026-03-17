---
type: concept
aliases: [SiLU, Swish]
---

# SiLU (Sigmoid Linear Unit)

## Intuition
SiLU 是一种平滑激活函数，形状比 ReLU 更连续，梯度变化更柔和。

## Why It Matters
更平滑的梯度常有利于对抗训练中的优化稳定性，减少梯度突变导致的训练不稳。

## Tiny Example
输入略小于 0 时，ReLU 直接截断为 0，而 SiLU 仍保留小幅连续响应。

## Definition
$$
\text{SiLU}(x)=x\cdot \sigma(x)
$$
其中 `sigma(x)` 是 sigmoid。

## Key Points
1. 非参数激活，不引入额外可学习系数。
2. 相比 ReLU 更平滑。
3. 在多个视觉任务中常与鲁棒性改进相关。

## How This Paper Uses It
- [[Robust Principles]]: 作为推荐激活替换 ReLU，并在多数据集鲁棒评估中得到稳定增益。

## Representative Papers
- [[Robust Principles]]: 对比 ReLU/GELU/参数化变体后推荐 SiLU。

## Related Concepts
- [[GELU]]
- [[Adversarial Robustness]]

