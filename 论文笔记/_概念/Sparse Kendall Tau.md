---
type: concept
aliases: [sKT, Sparse Kendall's Tau]
---

# Sparse Kendall Tau

## Intuition

Sparse Kendall Tau is a robust variant of rank correlation that ignores tiny prediction differences likely caused by noise, so ranking quality is measured in a more stable way.

## Why It Matters

In NAS prediction, many architectures have very close accuracies. Standard Kendall's Tau can over-penalize harmless swaps caused by tiny fluctuations.

## Tiny Example

If two architectures differ by only 0.03% predicted accuracy, sparse Kendall Tau can treat them as tied (after quantization), instead of counting it as a ranking mistake.

## Definition

Sparse Kendall Tau (sKT) computes Kendall rank correlation after coarsening scores at a fixed precision threshold (in NAS-Bench-301, 0.1% validation accuracy precision), reducing sensitivity to small noisy rank inversions.

## Math Form (if needed)

Given predicted accuracies y_hat, apply rounding:

y_hat' = round(y_hat / delta) * delta

Then compute Kendall's Tau on y_hat' and y_true.

- delta is the precision threshold (e.g., 0.1% accuracy).

## Key Points

1. Less sensitive to aleatoric noise than raw Kendall's Tau.
2. Better aligned with practical ranking quality when many candidates are near-ties.
3. Still captures large ordering errors.

## How This Paper Uses It

- [[NAS-Bench-301]]: Uses sKT together with R2 to evaluate surrogate fit and leave-one-optimizer-out generalization.

## Representative Papers

- [[NAS-Bench-301]]: Applies sKT for surrogate benchmark evaluation.
- [[Kendall's Tau]]: The base rank-correlation metric that sKT adapts.

## Related Concepts

- [[Kendall's Tau]]
- [[Surrogate Predictor]]
- [[Surrogate NAS Benchmark]]

