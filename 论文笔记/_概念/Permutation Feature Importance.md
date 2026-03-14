---
type: concept
aliases: [PFI, Permutation Importance]
---

# Permutation Feature Importance

## Intuition
To test how important one feature is, shuffle that feature and see how much model performance drops.

## Why It Matters
It provides model-agnostic interpretability and is often more faithful than raw tree impurity scores in correlated settings.

## Tiny Example
If shuffling `jacov` causes large R2 drop while shuffling `zen` barely changes R2, `jacov` is more important for the predictor.

## Definition
Permutation Feature Importance measures the expected performance degradation after random permutation of one feature, breaking its relation with the target while keeping the model fixed.

## Key Points
1. Works with many model types.
2. Importance is task-dependent and data-dependent.
3. Correlated features can share importance, so low single-feature importance does not always mean uselessness.

## How This Paper Uses It
- [[ZCP-Eval]]: Uses permutation analysis to show robust prediction needs multiple proxy features.

## Representative Papers
- [[Breiman Random Forests]]: Forest-based modeling context where permutation importance is widely used.
- [[ZCP-Eval]]: Applies it to robustness-oriented NAS proxy analysis.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Surrogate Predictor]]
- [[Robust Neural Architecture Search]]

