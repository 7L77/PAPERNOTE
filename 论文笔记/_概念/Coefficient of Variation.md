---
type: concept
aliases: [CV, Relative Dispersion]
---

# Coefficient of Variation

## Intuition
The coefficient of variation (CV) measures how noisy a quantity is relative to its own average scale. It answers: "Is this fluctuation small or large compared with the typical value?"

## Why It Matters
Raw variance is not directly comparable across metrics with different magnitudes. CV normalizes dispersion and makes stability comparisons fairer.

## Tiny Example
Model A scores around `100 +/- 5`, Model B scores around `10 +/- 5`. Both have the same absolute spread, but B is much less stable relative to its mean. CV captures that difference.

## Definition
For a random variable `X` with nonzero mean:

\[
\mathrm{CV}(X)=\frac{\mathrm{Std}(X)}{\mathrm{Mean}(X)}
\]

Some papers use `Var/Mean` as a scale-normalized dispersion proxy. Always check the exact definition used.

## Math Form (if needed)
- `Std(X)`: standard deviation of samples.
- `Mean(X)`: sample mean.
- Larger CV means larger relative instability.

## Key Points
1. CV is scale-aware; variance alone is not.
2. CV is meaningful only when the mean has a meaningful non-arbitrary zero and is not near zero.
3. CV is useful for comparing ranking-function stability across search spaces.

## How This Paper Uses It
- [[Variation-Matters]]: uses CV-based variation aggregation over architectures to quantify ranking-function variability (Sec. 4.1, Eq. 1).

## Representative Papers
- [[Variation-Matters]]: treats CV as a core statistic to characterize zero-shot ranking noise.

## Related Concepts
- [[Stochastic Dominance]]
- [[Mann-Whitney U Test]]
- [[Zero-Cost Proxy]]



