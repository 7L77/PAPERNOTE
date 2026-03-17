---
type: concept
aliases: [Conv Stem, Convolution Stem]
---

# Convolutional Stem

## Intuition
`Convolutional Stem` 是网络最前面的下采样与特征提取模块，通过卷积核滑窗来保留局部连续结构。

## Why It Matters
相比更激进的 token/patch 切分，卷积 stem 可通过重叠感受野与较温和步幅减少信息丢失，对鲁棒性有帮助。

## Tiny Example
`7x7 conv + stride 2` 再接后续 stage，通常比一次性 `patch=4, stride=4` 更保留局部边缘信息。

## Definition
在输入后使用卷积层（常带重叠）作为首个特征变换与下采样阶段，而非先做非重叠 patch 切块。

## Key Points
1. 关键不是“卷积”本身，而是下采样侵略性与重叠区域。
2. 常与 postponed downsampling 配合。
3. 可在参数变化较小的情况下带来鲁棒增益。

## How This Paper Uses It
- [[Robust Principles]]: 证明 convolutional stem 在对抗鲁棒性上整体优于 patchify stem。

## Representative Papers
- [[Robust Principles]]: 系统对比 conv stem 与 patchify stem 的鲁棒差异。

## Related Concepts
- [[Patchify Stem]]
- [[Adversarial Robustness]]

