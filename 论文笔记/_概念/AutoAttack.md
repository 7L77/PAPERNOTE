---
type: concept
aliases: [AA, Auto Attack]
---

# AutoAttack

## Intuition
`AutoAttack` 是一个标准化鲁棒评估攻击集合，不靠手调超参，而是用固定流程尽量避免“评估太弱”。

## Why It Matters
单一攻击容易高估模型鲁棒性；AutoAttack 用多种互补攻击组合，能更可靠地暴露脆弱性。

## Tiny Example
一个模型在 PGD 下看起来很稳，但在 AutoAttack 的组合攻击下可能明显掉点。

## Definition
AutoAttack 通常由多种参数无关或弱参数依赖的攻击组合而成，用统一协议报告鲁棒精度。

## Key Points
1. 目的是“可比性强、较难被调参误导”的鲁棒评估。
2. 常用作论文主表的鲁棒指标之一。
3. 与 PGD 互补，常联合报告。

## How This Paper Uses It
- [[Robust Principles]]: 以 AA 作为核心鲁棒指标之一，在 CIFAR 与 ImageNet 报告显著提升。

## Representative Papers
- [[Robust Principles]]: 在多架构和多训练方案下报告 AA 增益。

## Related Concepts
- [[PGD Attack]]
- [[RobustBench]]

