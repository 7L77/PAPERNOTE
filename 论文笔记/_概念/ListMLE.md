---
type: concept
aliases: [Listwise MLE, ListMLE Loss]
---

# ListMLE

## Intuition

ListMLE is a list-level ranking loss: instead of comparing items two by two, it asks the model to assign high probability to the whole ground-truth ranking order.

## Why It Matters

For NAS predictor training, we often care about the quality of the ranked list itself. ListMLE can capture global ordering behavior better than pointwise regression.

## Tiny Example

Suppose three architectures have true order A > B > C. ListMLE encourages the predictor scores to make this entire sequence likely, not just A>B and B>C separately.

## Definition

Given a permutation \(\pi\) sorted by ground-truth performance:
\[
\mathcal{L}_{ListMLE}=-\sum_{i=1}^{n}\log\frac{\exp(\hat{y}_{\pi(i)})}{\sum_{k=i}^{n}\exp(\hat{y}_{\pi(k)})}
\]
where \(\hat{y}\) is predicted score.

## Math Form (if needed)

- \(\pi(i)\): index at rank \(i\) in ground-truth ordering.
- \(\hat{y}_{\pi(i)}\): predicted score of that item.
- Lower loss means predicted scores are more consistent with the true ranking list.

## Key Points

1. It is a listwise loss, not pointwise/pairwise.
2. It optimizes ranking consistency over a whole list.
3. It can be more stable than pairwise losses when list-level ordering is the main target.

## How This Paper Uses It

- [[PWLNAS]]: uses ListMLE as a representative listwise baseline and as a warm-up component in piecewise loss on NAS-Bench-101.

## Representative Papers

- [[PWLNAS]]: comprehensive NAS-oriented comparison of ListMLE vs other loss families.

## Related Concepts

- [[Listwise Ranking Loss]]
- [[Pairwise Ranking Loss]]
