---
type: concept
aliases: [Patchify, Patch Stem]
---

# Patchify Stem

## Intuition
`Patchify Stem` 把输入图像切成固定大小且通常不重叠的 patch，然后把 patch 当作后续网络的基本输入单元。

## Why It Matters
它能快速降采样并减少计算，但过于激进时可能损失细粒度局部结构，从而影响对抗鲁棒性。

## Tiny Example
`patch=4, stride=4` 会把图像直接分成不重叠块；比起带重叠卷积，边缘细节更容易被抹平。

## Definition
通过一个 `kernel=p, stride=p` 的卷积（或等价操作）将图像切成 `p x p` patch 的 stem 设计。

## Key Points
1. 计算效率高，但信息保留依赖 patch 大小与重叠策略。
2. 缺乏重叠时更容易损失局部连续性。
3. 与卷积 stem 的对比常用于解释鲁棒性差异。

## How This Paper Uses It
- [[Robust Principles]]: 作为对照 stem，整体鲁棒性弱于 convolutional stem。

## Representative Papers
- [[Robust Principles]]: 在鲁棒评估中系统比较 patchify 与 convolutional stem。

## Related Concepts
- [[Convolutional Stem]]
- [[Adversarial Robustness]]

