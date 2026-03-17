---
type: concept
aliases: [RSO, Multi-strength robust objective]
---

# Robust Search Objective

## Intuition

Architecture search needs a scalar objective. For robust NAS across multiple strengths, we combine clean loss and several adversarial losses with explicit balancing weights.

## Why It Matters

Without a balancing objective, search may overfit either clean accuracy or one strong-attack point. A robust objective defines the tradeoff directly.

## Tiny Example

If two architectures have similar clean loss, the one with lower weighted multi-strength adversarial losses should be preferred during search.

## Definition

A robust search objective is a weighted aggregation:
\[
\mathcal{J}(A)=\alpha \hat{L}_{natural}(A)+\beta\sum_i \beta_i \hat{L}_{\epsilon_i}(A),
\]
where \(A\) is architecture parameter, \(\alpha+\beta=1\), \(\sum_i\beta_i=1\).

## Math Form (if needed)

In Wsr-NAS this objective is optimized over architecture weights, while losses are predicted by VLE in EWSS.

## Key Points

1. \(\alpha,\beta\) control global clean-vs-robust tradeoff.
2. \(\beta_i\) allocates emphasis among strengths.
3. Weight normalization is important for stable optimization.

## How This Paper Uses It

- [[Wsr-NAS]]: Uses Eq.(10) to update supernet architecture parameters with clean and multi-strength robust losses.

## Representative Papers

- [[Wsr-NAS]]: Presents a practical robust objective integrated with predictor-based architecture update.

## Related Concepts

- [[Validation Loss Estimator]]
- [[Wide Spectrum Adversarial Robustness]]
- [[One-shot NAS]]
- [[Adversarial Robustness]]

