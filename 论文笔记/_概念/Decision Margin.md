---
type: concept
aliases: [Logit Margin, Classification Margin]
---

# Decision Margin

## Intuition

Decision Margin measures how much more confident a classifier is in the true class than in the strongest competing class.  
If this gap is small, a tiny perturbation may flip the prediction.

## Why It Matters

It is a direct signal of boundary proximity and is often used to estimate robustness risk per sample.

## Tiny Example

If logits are `[cat=4.2, dog=3.9, bird=0.8]` and label is `cat`, margin is `4.2-3.9=0.3`.  
A perturbation that raises `dog` slightly can cross the boundary.

## Definition

For sample \(x\) with true label \(y\), margin is:
\[
M_\theta^y(x)=\ell_\theta^y(x)-\max_{y'\neq y}\ell_\theta^{y'}(x)
\]
where \(\ell_\theta^c(x)\) is the class-\(c\) logit.

## Math Form (if needed)

Large positive margin usually means the sample is farther from the current decision boundary under the model.

## Key Points

1. Margin is sample-specific and model-state-specific.
2. Margin is sensitive to training progress and attack strategy.
3. Margin differences (clean vs. adversarial) can reveal vulnerability.

## How This Paper Uses It

- [[VDAT]]: Uses clean/adv margin difference to define vulnerability and drive sample-wise filtering.

## Representative Papers

- [[VDAT]]: Builds a vulnerability score from margin shifts.
- [[Robust Principles]]: Discusses boundary-related robustness behavior from architecture perspective.

## Related Concepts

- [[Adversarial Training]]
- [[PGD Attack]]

