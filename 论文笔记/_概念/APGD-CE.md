---
type: concept
aliases: [Auto-PGD CE, APGD Cross-Entropy]
---

# APGD-CE

## Intuition
APGD-CE is a strong iterative gradient attack that adapts step sizes automatically while maximizing cross-entropy loss.

## Why It Matters
It is usually stronger than simple one-step attacks and is a core component in robust evaluation pipelines like AutoAttack.

## Tiny Example
Instead of one FGSM step, APGD-CE performs many projected steps and adjusts step size when progress stalls, often finding harder adversarial examples.

## Definition
APGD-CE (Auto-Projected Gradient Descent with cross-entropy objective) solves a norm-constrained inner maximization via iterative projected updates and adaptive step control.

## Key Points
1. Strong white-box baseline for robustness testing.
2. Uses projection to stay within epsilon-ball constraints.
3. Choice of objective (CE vs DLR) can change attack strength on some models.

## How This Paper Uses It
- [[Padding-Robustness Interplay]]: APGD-CE is used in standalone evaluation and inside AutoAttack; zero padding often ranks best on this specific attacker.

## Representative Papers
- [[AutoAttack]]: Introduces APGD variants in a standardized evaluation suite.

## Related Concepts
- [[AutoAttack]]
- [[Adversarial Robustness]]

