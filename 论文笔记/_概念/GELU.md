---
type: concept
aliases: [Gaussian Error Linear Unit]
---

# GELU

## Intuition
GELU 可以理解为“按输入大小做平滑门控”的激活，而非硬阈值裁剪。

## Why It Matters
它常用于 Transformer，也被用于替换 ReLU 来提升训练稳定性和表示平滑性。

## Tiny Example
对接近 0 的输入，GELU 不会像 ReLU 一样突然截断，输出变化更连续。

## Definition
常见近似：

$$
\text{GELU}(x)\approx 0.5x\left(1+\tanh\left[\sqrt{2/\pi}(x+0.044715x^3)\right]\right)
$$

## Key Points
1. 平滑非线性，梯度较连续。
2. 在视觉与语言模型都常见。
3. 常作为 ReLU 的平滑替代。

## How This Paper Uses It
- [[Robust Principles]]: 作为平滑激活候选之一，表现优于 ReLU。

## Representative Papers
- [[Robust Principles]]: 在鲁棒架构实验中比较了 GELU 与其他激活。

## Related Concepts
- [[SiLU (Sigmoid Linear Unit)]]
- [[Adversarial Robustness]]

