---
type: concept
aliases: [NASRobBench201, Robust NAS-Bench-201]
---

# NAS-Rob-Bench-201

## Intuition
NAS-Rob-Bench-201 is a robust NAS benchmark that precomputes adversarially trained performance for a large architecture set, so robust search methods can be compared by lookup instead of repeated expensive retraining.

## Why It Matters
It provides a controlled testbed for robust architecture search, reducing repeated adversarial training cost and helping isolate the quality of search strategies.

## Tiny Example
In robust NAS studies, different search algorithms can be run with the same query budget on NAS-Rob-Bench-201 and compared directly on PGD/FGSM robustness metrics.

## Definition
NAS-Rob-Bench-201 is built on NAS-Bench-201 search space and reports adversarially trained performance for 6466 non-isomorphic architectures, including clean and robust metrics (e.g., FGSM/PGD/APGD variants).

## Key Points
1. It is a tabular robust benchmark over a fixed NAS search space.
2. It supports fair, budget-controlled robust NAS comparisons.
3. It is designed for reproducibility and efficient algorithm assessment.

## How This Paper Uses It
- [[NAS-RobBench-201]] introduces and analyzes this benchmark.
- [[TRNAS]] uses NAS-Rob-Bench-201 for direct comparison against standard and robust NAS methods under fixed evaluation budgets.

## Representative Papers
- [[NAS-RobBench-201]] defines this benchmark.
- [[TRNAS]] uses it to validate robust-search efficiency and effectiveness.

## Related Concepts
- [[RobustBench]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]
