---
type: concept
aliases: [HRS]
---

# Harmonic Robustness Score

## Intuition
HRS is a joint metric that rewards models only when both clean accuracy and adversarial robustness are high.

## Why It Matters
Using only one metric can hide tradeoffs; HRS penalizes imbalance and highlights methods that are strong on both fronts.

## Tiny Example
A model with very high clean accuracy but weak robustness can get lower HRS than a more balanced model.

## Definition
HRS is a combined score built from natural accuracy and adversarial robustness using a harmonic-style aggregation (as adopted in REP experiments).

## Key Points
1. Encourages balanced performance instead of single-metric overfitting.
2. Useful for robust NAS evaluation where clean/robust tradeoff is central.
3. Best interpreted alongside per-attack robustness metrics.

## How This Paper Uses It
- [[REP]] reports HRS in CNN/GNN comparisons and achieves the best HRS across reported settings.

## Representative Papers
- [[REP]]: Uses HRS to evaluate overall robustness-quality balance.

## Related Concepts
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Neural Architecture Search]]
