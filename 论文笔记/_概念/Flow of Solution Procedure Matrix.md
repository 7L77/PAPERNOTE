---
type: concept
aliases: [FSP Matrix, FSP]
---

# Flow of Solution Procedure Matrix

## Intuition
FSP Matrix summarizes how information flows from a layer's input feature map to its output feature map. If this flow changes a lot under adversarial perturbation, the network is likely less robust.

## Why It Matters
It provides a layer-wise structural signal for robustness screening, instead of only checking final prediction accuracy.

## Tiny Example
For the same image, compute a layer's FSP on clean input and on adversarial input. If deeper layers show a large gap, that architecture is often more sensitive to attacks.

## Definition
For layer/cell `l`, the FSP matrix is the normalized inner product between input and output feature maps over spatial positions:
\[
G_l(x;\theta)=\frac{1}{h\times w}\sum_{s=1}^{h}\sum_{t=1}^{w}F^{in}_{l,s,t}(x;\theta)\cdot F^{out}_{l,s,t}(x;\theta)
\]
Robustness-related FSP distance is commonly computed between clean and adversarial inputs:
\[
L_l^{FSP}=\frac{1}{N}\sum_x \|G_l(x;\theta)-G_l(x';\theta)\|_2^2
\]

## Key Points
1. It captures feature-flow consistency, not just output logits.
2. In RobNet, deeper-layer FSP distance is more correlated with robustness gap.
3. It can be used as a low-cost filter before expensive finetuning/evaluation.

## How This Paper Uses It
- [[RobNet]]: Uses FSP distance in deeper cells to filter non-robust architectures in cell-free search.

## Representative Papers
- [[RobNet]]: Uses FSP distance as a robustness indicator for architecture filtering.

## Related Concepts
- [[Adversarial Robustness]]
- [[Cell-based Search Space]]
- [[Neural Architecture Search]]

