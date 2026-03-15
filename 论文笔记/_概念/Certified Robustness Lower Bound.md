---
type: concept
aliases: [Certified Lower Bound, Certified Adversarial Robustness Lower Bound]
---

# Certified Robustness Lower Bound

## Intuition

It is a guaranteed minimum safety margin: instead of testing only a few attacks, we prove that within a perturbation radius, the model output cannot cross a wrong decision boundary below a certain bound.

## Why It Matters

Attack-based evaluation can miss stronger attacks. A certified lower bound gives a worst-case guarantee and is harder to game.

## Tiny Example

Suppose a classifier predicts class A over class B with margin 0.12, and bound analysis proves perturbations up to `epsilon=0.05` cannot reduce this margin below 0.02. Then robustness is not just empirical; it is certified in that neighborhood.

## Definition

For an input and perturbation set (e.g., `||delta||_p <= epsilon`), compute a provable lower bound on the classification margin/logit gap. If the lower bound stays positive, prediction is certifiably robust under that threat model.

## Math Form (if needed)

Let `m(x, delta)` be margin between true class and strongest competitor under perturbation `delta`. A certified method derives:

\[
\underline{m}(x) \le \min_{\|\delta\|_p \le \epsilon} m(x,\delta)
\]

If \(\underline{m}(x) > 0\), the sample is certified robust at radius `epsilon`.

## Key Points

1. It is a guarantee, not a sampled attack result.
2. Tighter bounds are better, but often more expensive to compute.
3. Certification strength depends on threat model (`p`-norm, radius, network assumptions).

## How This Paper Uses It

- [[DSRNA]]: Uses certified lower bounds from block-wise linear bounds as a differentiable architecture robustness metric in NAS.

## Representative Papers

- [[CNN-Cert]]: Efficient certified robustness bounds for CNNs via linear bounding and composition.

## Related Concepts

- [[Adversarial Robustness]]
- [[Jacobian Norm Bound]]
