---
type: concept
aliases: [Robustness to Adversarial Attacks, Adversarial Stability]
---

# Adversarial Robustness

## Intuition
Adversarial robustness is a model's ability to keep correct predictions when inputs are intentionally perturbed in hard-to-detect ways.

## Why It Matters
Small perturbations can cause confident errors. Robustness is required for reliable deployment in high-stakes systems.

## Tiny Example
An image classifier predicts "cat" on a clean image, but after tiny PGD perturbation predicts "truck"; this indicates poor adversarial robustness.

## Definition
Adversarial robustness quantifies model performance under worst-case perturbations constrained by a norm bound (e.g., Linf epsilon), typically evaluated by attack success rates or robust accuracy.

## Key Points
1. Robustness and clean accuracy are related but not equivalent.
2. Attack strength/type (FGSM, PGD, APGD, AutoAttack) changes measured robustness.
3. Robust evaluation is more expensive than clean evaluation.

## How This Paper Uses It
- [[ZCP-Eval]]: Treats robust accuracy as prediction targets and analyzes transferability of zero-cost proxies.

## Representative Papers
- [[Explaining and Harnessing Adversarial Examples]]: Foundational adversarial-example work.
- [[AutoAttack]]: Strong standardized attack suite.

## Related Concepts
- [[Robust Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]

