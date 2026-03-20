---
type: concept
aliases: [Mean Absolute Percentage Error Loss, MAPE]
---

# MAPE Loss

## Intuition

MAPE Loss measures relative error rather than absolute error. In NAS predictor training, this can emphasize mistakes around high-performing architectures when formulated in error space.

## Why It Matters

Top architectures often have close absolute accuracies. Relative-error style weighting can better separate these strong candidates.

## Tiny Example

If two predictions have the same absolute error, the one with larger relative error to its target receives higher penalty under MAPE-style objectives.

## Definition

In the PWLNAS implementation, MAPE is used on error terms:
\[
\mathcal{L}_{MAPE}=\frac{1}{n}\sum_i\left|\frac{(1-\hat{y}_i)-b}{(1-y_i)-b}-1\right|
\]
where \(b\) is a lower-bound stabilizer.

## Math Form (if needed)

- \(y_i\): ground-truth accuracy.
- \(\hat{y}_i\): predicted accuracy.
- \(1-y\): transformed error.
- \(b\): lower bound to avoid unstable denominators near zero.

## Key Points

1. It is a weighted/relative perspective, not plain squared error.
2. It can improve top-ranking precision with sufficient training data.
3. Its effect depends on predictor backbone and search space.

## How This Paper Uses It

- [[PWLNAS]]: uses MAPE as a key weighted loss, and in piecewise settings such as HR -> MAPE on NAS-Bench-201 and DARTS.

## Representative Papers

- [[PWLNAS]]: systematic study of when MAPE helps predictor-based NAS.

## Related Concepts

- [[Piecewise Loss Function]]
- [[WARP Loss]]
