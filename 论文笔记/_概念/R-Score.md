---
type: concept
aliases: [Robustness Score, TRNAS R-Score]
---

# R-Score

## Intuition
R-Score is a training-free proxy that tries to estimate how robust an architecture may be before expensive adversarial training.

## Why It Matters
Robust NAS is expensive because each candidate typically needs adversarial training. A useful pre-training robustness score can drastically cut search cost.

## Tiny Example
If architecture A and B have similar clean proxy quality, but A has a higher R-Score, TRNAS prioritizes A for evolutionary selection and final robust training.

## Definition
In TRNAS, R-Score combines:
1. a local perturbation-sensitive component (linear activation capability),
2. a global feature-stability component (feature consistency).
The final proxy is a weighted sum:
`R = beta * LAM + (1 - beta) * FRM`.

## Key Points
1. It is designed for robustness-aware ranking, not just clean accuracy ranking.
2. It is computed in the training-free stage.
3. It is used together with multi-objective selection to stabilize search.

## How This Paper Uses It
- [[TRNAS]] uses R-Score to prune and rank candidates in the DARTS search space before full adversarial training.

## Representative Papers
- [[TRNAS]]: introduces R-Score for training-free robust architecture search.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[RobustBench]]

