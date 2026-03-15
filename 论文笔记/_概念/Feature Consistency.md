---
type: concept
aliases: [Robust Feature Consistency, Cross-perturbation Feature Consistency]
---

# Feature Consistency

## Intuition
A robust model should produce similar semantic features for a clean input and its perturbed counterpart.

## Why It Matters
If features drift too much under perturbation, downstream classifier decisions become unstable.

## Tiny Example
If `x` is a clean image and `x'` is FGSM-perturbed, a robust encoder keeps `cos(e(x), e(x'))` high.

## Definition
Feature consistency measures similarity between representations extracted from clean and perturbed samples, usually layer-wise.

## Key Points
1. It is a representation-level robustness signal.
2. It can be measured without full training.
3. It should be evaluated across diverse perturbations, not only one attack.

## How This Paper Uses It
- [[CRoZe]] defines layer-wise feature similarity `Z_m` and uses it as one component of the final proxy (Eq. 5, Eq. 10).

## Representative Papers
- [[CRoZe]]: Uses feature consistency for robust NAS proxy design.

## Related Concepts
- [[Parameter Consistency]]
- [[Gradient Alignment]]
- [[Adversarial Robustness]]
