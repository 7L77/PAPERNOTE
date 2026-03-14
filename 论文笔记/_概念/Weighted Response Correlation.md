---
type: concept
aliases: [WRCor, Weighted Correlation of Responses]
---

# Weighted Response Correlation

## Intuition

`Weighted Response Correlation (WRCor)` 的核心想法是：一个好架构应当让不同输入样本在网络中的响应（激活与梯度）更容易区分；如果不同样本的响应总是高度相关，模型就更难学到有判别性的表示。

## Why It Matters

在 training-free NAS 里，我们希望不训练就估计架构好坏。WRCor 提供了一个只靠初始化网络前后向即可计算的标量分数，能大幅降低搜索成本。

## Tiny Example

设有两个候选网络 A/B，对同一批样本计算响应相关矩阵：

- A 的非对角元素整体更小（样本间更不相似）
- B 的非对角元素整体更大（样本间更“挤在一起”）

则 WRCor 倾向给 A 更高分，表示 A 更可能有更强判别能力。

## Definition

WRCor 是对多层响应相关矩阵做层级加权聚合后，再取 log-determinant 的代理分数。常见形式：

\[
S_{\text{WRCor}}=\log(\det(K)),
\quad
K=\sum_{l}\sum_{i}2^l\left(|C^{A}_{l,i}|+|C^{G}_{l,i}|\right)
\]

其中 \(C^A\) 与 \(C^G\) 分别是激活与梯度的样本相关矩阵。

## Math Form (if needed)

- \(2^l\)：层权重，强调高层响应（top-level features）。
- \(|C|\)：取绝对相关，避免正负相关抵消。
- \(\log\det(\cdot)\)：把矩阵结构映射成稳定可比较的标量。

## Key Points

1. 同时结合 expressivity（激活）和 generalizability（梯度）信号。
2. 相比不加权 RCor，更强调高层响应区分能力。
3. 能直接作为 zero-shot NAS 的打分函数。

## How This Paper Uses It

- [[WRCor]]: 作为核心 training-free proxy，并与 SynFlow/JacCor/PNorm 组合成投票代理用于搜索。

## Representative Papers

- [[WRCor]]: 系统提出 ACor/RCor/WRCor 及其在 NAS-Bench/MobileNetV2 上的验证。

## Related Concepts

- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Network Expressivity]]
- [[Spearman's Rank Correlation]]


