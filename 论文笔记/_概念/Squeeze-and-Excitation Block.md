---
type: concept
aliases: [SE Block, SE]
---

# Squeeze-and-Excitation Block

## Intuition
SE 模块是“按通道做注意力重标定”：先看每个通道全局统计，再给通道乘上不同权重，让有用通道更突出。

## Why It Matters
它几乎不改主干拓扑，却能提升特征表达质量；在鲁棒场景中也可能增强关键特征通道的稳定性。

## Tiny Example
若某些通道在目标类别上更稳定，SE 会给这些通道更大权重，减弱噪声敏感通道影响。

## Definition
典型形式是：
1. `Squeeze`: 对每个通道做全局池化得到通道描述。
2. `Excitation`: 通过小 MLP 生成通道权重。
3. `Scale`: 将权重乘回原特征图。

## Math Form (if needed)
设输入特征 `X in R^{C x H x W}`，通道描述为：

$$
z_c=\frac{1}{HW}\sum_{i=1}^{H}\sum_{j=1}^{W}X_{c,i,j}
$$

再经 `g(z)=\sigma(W_2 \delta(W_1 z))` 得到通道权重并回乘。

## Key Points
1. 关键超参是 reduction ratio `r`（控制中间瓶颈宽度）。
2. `r` 过大可能压缩过强，损害表达与鲁棒性。
3. 作为插件模块，工程落地成本较低。

## How This Paper Uses It
- [[Robust Principles]]: 在 ImageNet 上发现 SE 对鲁棒性有稳定正增益，并推荐较小 `r`（如 `r=4`）。

## Representative Papers
- [[Robust Principles]]: 在对抗训练语境下分析 SE 的 reduction ratio 影响。

## Related Concepts
- [[Convolutional Stem]]
- [[Adversarial Robustness]]

