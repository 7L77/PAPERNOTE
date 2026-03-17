---
type: concept
aliases: [GZSL, Generalised Zero-Shot Learning]
---

# Generalized Zero-Shot Learning

## Intuition
GZSL is a harder version of ZSL: the model must classify both seen and unseen classes at test time, so it must avoid over-predicting seen classes.

## Why It Matters
Real deployments rarely have a test stream containing only unseen classes. GZSL better reflects practical open-world recognition settings.

## Tiny Example
In testing, images may come from both seen classes (horse, zebra) and unseen classes (okapi). A model that predicts seen classes for everything has high seen accuracy but fails GZSL.

## Definition
Under disjoint seen/unseen training sets, GZSL predicts over `Y_s ∪ Y_u` at test time. Performance is commonly reported using seen accuracy `A_s`, unseen accuracy `A_u`, and harmonic mean `A_h`.

## Key Points
1. GZSL balances seen/unseen performance, not only unseen accuracy.
2. Harmonic mean penalizes strong imbalance between `A_s` and `A_u`.
3. Architecture or loss improvements should be judged by both `A_s` and `A_u`.

## How This Paper Uses It
- [[ZeroNAS]]: Reports GZSL improvements on CUB/FLO/SUN/AWA and shows better seen-unseen balance with searched architectures.

## Representative Papers
- [[ZeroNAS]]: Evaluates searched GAN structures with `A_s`, `A_u`, and `A_h`.

## Related Concepts
- [[Zero-Shot Learning]]
- [[Generative Adversarial Network]]
- [[Neural Architecture Search]]
