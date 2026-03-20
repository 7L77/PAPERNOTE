---
type: concept
aliases: [CO in Fast Adversarial Training]
---

# Catastrophic Overfitting

## Intuition

In single-step adversarial training, a model can suddenly appear robust during training but actually collapses under stronger multi-step attacks.

## Why It Matters

It creates a false sense of robustness and can invalidate training-time conclusions.

## Tiny Example

A model trained with FGSM reaches high FGSM accuracy, but PGD accuracy drops sharply after a certain epoch.

## Definition

Catastrophic Overfitting is a training instability where robustness against strong attacks abruptly degrades, often in fast/single-step adversarial training regimes.

## Math Form (if needed)

Operationally, it is detected via divergence between weak-attack and strong-attack validation curves.

## Key Points

1. It is common in fast adversarial training if stabilization is insufficient.
2. Monitoring only FGSM is risky; PGD/AA tracking is necessary.
3. Data filtering and training dynamics can influence its occurrence.

## How This Paper Uses It

- [[VDAT]]: Reports that iterative sample filtering does not induce catastrophic overfitting in their experiments.

## Representative Papers

- [[VDAT]]: Empirical evidence under sample-wise filtering.

## Related Concepts

- [[Adversarial Training]]
- [[AutoAttack]]

