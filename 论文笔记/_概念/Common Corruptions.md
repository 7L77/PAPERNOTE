---
type: concept
aliases: [Image Corruptions, Common Corruptions Benchmark]
---

# Common Corruptions

## Intuition
Common corruptions are non-adversarial but realistic visual degradations such as noise, blur, weather, and digital artifacts.

## Why It Matters
Robust deployment needs models that survive distribution shifts beyond clean test sets and beyond attack-only evaluation.

## Tiny Example
A model can do well on clean CIFAR-10 and still fail badly under fog, Gaussian noise, or motion blur.

## Definition
Common corruptions are standardized perturbation families (often from ImageNet-C/CIFAR-C style benchmarks) used to evaluate robustness under natural distribution shifts.

## Key Points
1. They are not crafted per-sample adversarial attacks.
2. They test broad robustness under realistic degradations.
3. Robust NAS should consider both adversarial and common corruption settings.

## How This Paper Uses It
- [[CRoZe]] evaluates robustness not only on adversarial attacks but also on 15 common corruption types across datasets.

## Representative Papers
- [[CRoZe]]
- [[Robust Neural Architecture Search]]

## Related Concepts
- [[Adversarial Robustness]]
- [[Harmonic Robustness Score]]
- [[Neural Architecture Search]]
