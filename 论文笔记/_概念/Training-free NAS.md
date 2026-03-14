---
type: concept
aliases: [Zero-shot NAS, Training Free NAS]
---

# Training-free NAS

## Intuition
Training-free NAS searches architectures by proxy signals instead of fully training each candidate.

## Why It Matters
It can reduce search cost from GPU-days to minutes/hours in many benchmark settings.

## Tiny Example
Instead of training 3,000 architectures, a method computes proxy scores for all candidates and only trains the top few.

## Definition
Training-free NAS is a class of NAS approaches that estimate architecture quality without iterative full training during the search phase.

## Math Form (if needed)
Typical objective is to maximize a proxy-based ranking score under resource constraints.

## Key Points
1. Search is decoupled from expensive full training.
2. Proxy quality determines final search quality.
3. Usually paired with evolutionary or random search loops.

## How This Paper Uses It
- [[AZ-NAS]]: Uses four complementary proxies plus non-linear rank aggregation in a training-free evolutionary framework.

## Representative Papers
- TE-NAS (ICLR 2021).
- AZ-NAS (CVPR 2024).

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]

