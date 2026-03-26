---
type: concept
aliases: [ECA, Efficient Channel Attention Module]
---

# Efficient Channel Attention

## Intuition

ECA（Efficient Channel Attention）是一种轻量通道注意力：不做大 MLP 压缩，仅通过局部 1D 卷积在通道维建模相关性，给每个通道一个权重。

## Why It Matters

相比 SE/CBAM 一类注意力，ECA 参数更少、引入的优化负担更小，适合放在 NAS 或鲁棒训练这种本身就昂贵的流程中。

## Tiny Example

如果某些通道在对抗样本上更稳定，ECA 会给这些通道更高权重；不稳定通道权重降低，从而提升鲁棒特征占比。

## Definition

给定特征图 \(U\in \mathbb{R}^{C\times H\times W}\)，先做全局平均池化：
\[
z=\mathrm{GAP}(U)\in\mathbb{R}^{C}
\]
再做 1D 卷积和 sigmoid：
\[
w=\sigma(\mathrm{Conv1D}(z))
\]
最后通道重标定：
\[
F=w\odot U
\]

## Math Form (if needed)

ECA 的关键是“局部跨通道交互 + 无瓶颈降维”。

## Key Points

1. 轻量、参数少，适合搜索过程。
2. 在不显著增算力的情况下提升通道选择能力。
3. 对鲁棒任务中“哪些特征该保留”很有效。

## How This Paper Uses It

- [[RDNAS]]: 在 dual-branch 输出融合处使用 ECA，自适应平衡 normal/robust 两路特征。

## Representative Papers

- [[RDNAS]]: 作为双分支融合模块，消融显示优于无注意力版本。

## Related Concepts

- [[Attention Map]]
- [[Adversarial Robustness]]
