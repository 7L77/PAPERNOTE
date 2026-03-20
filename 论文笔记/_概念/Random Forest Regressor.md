---
type: concept
aliases: [RF Regressor, Random Forest Regression]
---

# Random Forest Regressor

## Intuition
A random forest regressor averages predictions from many decision trees, so each tree makes a rough guess and the ensemble gives a more stable estimate.

## Why It Matters
For NAS proxy prediction, labels are noisy and feature interactions are non-linear. Random forests are robust, easy to tune, and often strong with modest data.

## Tiny Example
Suppose we want to predict robust accuracy from `jacov`, `snip`, and `flops`. Different trees split on different feature subsets; averaging their outputs reduces overfitting compared with a single tree.

## Definition
Random Forest Regressor is an ensemble regression model that trains multiple bootstrapped decision trees with feature subsampling and outputs the mean prediction across trees.

## Key Points
1. Works well on tabular features with non-linear interactions.
2. Usually needs little feature scaling.
3. Can provide feature-importance signals, but different importance definitions (MDI vs permutation) may lead to different interpretations.

## How This Paper Uses It
- [[ZCP-Eval]]: Uses random forest to map multi-proxy vectors to clean and robust accuracy targets under different train sizes.

## Representative Papers
- [[ZCP-Eval]]: Applies random forest to robustness-oriented proxy prediction in NAS.
- Breiman (2001): Original random forest formulation.

## Related Concepts
- [[Surrogate Predictor]]
- [[Permutation Feature Importance]]
- [[Neural Architecture Search]]
