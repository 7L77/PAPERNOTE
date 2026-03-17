---
type: concept
aliases: [WD Ratio, Width Depth Ratio]
---

# Width-Depth Ratio

## Intuition
`Width-Depth Ratio` 用来描述一个分阶段 CNN 在“每层有多宽、每个 stage 有多深”之间的平衡。它把“宽而浅”与“窄而深”的差异压缩成一个可比较的数字。

## Why It Matters
在鲁棒训练中，网络容量不只是参数总量问题，容量如何分配到宽度与深度也会改变对抗泛化与优化稳定性。

## Tiny Example
如果两个网络参数量接近，但一个把预算放在更大通道数，另一个放在更多层，二者对同一攻击预算下的鲁棒精度可能显著不同。

## Definition
对 `n` 个 stage 的网络，排除最后一个 stage：

$$
\text{WD ratio}=\frac{1}{n-1}\sum_{i=1}^{n-1}\frac{W_i}{D_i}
$$

其中 `W_i` 是第 `i` 个 stage 的宽度（通道相关量），`D_i` 是该 stage 的深度（块数）。

## Key Points
1. WD ratio 反映的是“分配结构”，不是总参数量本身。
2. 它能跨不同 stage 数量进行比较。
3. 在鲁棒 CNN 设计里，常用于筛选更稳健的宽深组合。

## How This Paper Uses It
- [[Robust Principles]]: 提出并验证 WD ratio 的鲁棒最优区间约 `[7.5, 13.5]`。

## Representative Papers
- [[Robust Principles]]: 明确提出 WD ratio 作为鲁棒架构尺度指标。

## Related Concepts
- [[Lipschitz Constant]]
- [[Adversarial Robustness]]

