---
type: concept
aliases: [Pairwise Loss, Pairwise Ranking Objective]
---

# Pairwise Ranking Loss

## Intuition

Pairwise ranking loss learns order by comparing samples in pairs: if sample A should outrank B, the model is penalized when predicted scores violate this relation.

## Why It Matters

Many NAS pipelines need reliable relative ordering more than exact performance values, especially under low-query settings.

## Tiny Example

If true performance says A>B but predictor gives \(\hat{y}_A < \hat{y}_B\), pairwise loss adds penalty to correct this pair.

## Definition

General form:
\[
\mathcal{L}_{pair}=\frac{1}{|\mathcal{N}|}\sum_{(i,j)\in\mathcal{N}} \ell\!\left(s_{ij}(\hat{y}_i-\hat{y}_j)\right)
\]
where \(s_{ij}\in\{-1,1\}\) encodes true order and \(\ell\) can be hinge/logistic variants.

## Math Form (if needed)

- HR: \(\ell(z)=\max(0,m-z)\).
- LR: \(\ell(z)=\log(1+\exp(-z))\).
- These losses focus on ordering correctness of sampled pairs.

## Key Points

1. Strong in low-data phases where absolute calibration is hard.
2. Optimizes local pair consistency, not full-list structure.
3. Frequently used as warm-up in staged NAS predictor training.

## How This Paper Uses It

- [[PWLNAS]]: compares HR/LR/MSE+SR as pairwise-family losses and uses HR in several piecewise settings.

## Representative Papers

- [[PWLNAS]]: highlights when pairwise losses outperform weighted losses in extremely low-data regimes.

## Related Concepts

- [[Listwise Ranking Loss]]
- [[Kendall's Tau]]
