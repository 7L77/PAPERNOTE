---
type: concept
aliases: [NASRobBench201, Robust NAS-Bench-201]
---

# NAS-Rob-Bench-201

## Intuition
NAS-Rob-Bench-201 is a robust NAS benchmark that precomputes adversarially trained performance for a complete architecture set, so search methods can be compared quickly.

## Why It Matters
It provides a controlled testbed for robust architecture search, reducing repeated adversarial training cost and helping isolate search strategy quality.

## Tiny Example
In TRNAS supplementary experiments, all compared NAS methods are transferred to NAS-Rob-Bench-201 with the same evaluation budget, enabling direct efficiency and performance comparison.

## Definition
NAS-Rob-Bench-201 contains 15,625 fully adversarially trained architectures in a NAS-Bench-201-style space and reports clean/robust metrics under several attack settings.

## Key Points
1. It is architecture-complete for its defined search space.
2. It supports robust NAS algorithm transfer and fair budgeted comparisons.
3. Minor random-seed effects can slightly change the observed best architecture performance.

## How This Paper Uses It
- [[TRNAS]] uses NAS-Rob-Bench-201 for direct comparison against standard and robust NAS methods under a fixed 1000-evaluation budget.

## Representative Papers
- Robust NAS under adversarial training benchmark paper (ICLR 2024) defines this benchmark.
- [[TRNAS]] uses it to validate robust-search efficiency and effectiveness.

## Related Concepts
- [[RobustBench]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]

