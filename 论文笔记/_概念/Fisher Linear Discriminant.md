---
type: concept
aliases: [FLD, Linear Discriminant]
---

# Fisher Linear Discriminant

## Intuition
FLD finds projection directions that maximize class separation while minimizing within-class spread.

## Why It Matters
It gives a principled balance between "between-class distance" and "within-class variance", which inspires robust hyperparameter heuristics.

## Tiny Example
If two classes have similar means but large overlap variance, FLD avoids overconfident separation; if means differ clearly with tight variance, separation score increases.

## Definition
In classic form, FLD seeks projection `w` maximizing:
\[
J(w)=\frac{w^T S_B w}{w^T S_W w}
\]
where `S_B` is between-class scatter and `S_W` is within-class scatter.

## Key Points
1. Emphasizes signal-to-noise style separation.
2. Historically used in classification and feature extraction.
3. Its ratio form appears in many modern statistical heuristics.

## How This Paper Uses It
- [[RBFleX-NAS]] states HDA is inspired by FLD-style separation logic.
- Candidate gamma uses mean-gap over variance terms, echoing FLD intuition.

## Representative Papers
- [[RBFleX-NAS]]
- Classical FLD / LDA literature.

## Related Concepts
- [[Hyperparameter Detection Algorithm]]
- [[Radial Basis Function Kernel]]

