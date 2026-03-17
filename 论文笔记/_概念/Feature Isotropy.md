---
type: concept
aliases: [Representation Isotropy, Isotropic Features]
---

# Feature Isotropy

## Intuition

Feature isotropy describes whether learned features spread more evenly across directions in representation space, instead of collapsing into a few dominant directions.

## Why It Matters

More isotropic representations are often associated with better transfer and generalization, especially in low-label settings.

## Tiny Example

If embeddings of samples occupy a broad, balanced cloud in many directions, isotropy is high; if they lie near a thin line, isotropy is low.

## Definition

Feature isotropy can be measured from the eigenvalue spectrum of a feature covariance/feature matrix: more uniform normalized eigenvalues imply higher isotropy.

## Math Form (if needed)

A common proxy is entropy of normalized eigenvalues:

\[
E = \sum_i -\bar{\lambda}_i \log(\bar{\lambda}_i)
\]

Higher entropy indicates more even spectral energy distribution.

## Key Points

1. Isotropy focuses on geometric distribution of features.
2. It is not identical to accuracy but may correlate with generalization.
3. Spectral entropy is a practical and cheap indicator in proxy-based methods.

## How This Paper Uses It

- [[GEN-TPC-NAS]]: Defines Entropy score from per-head feature spectra to approximate generalization ability.

## Representative Papers

- [[GEN-TPC-NAS]]: Uses isotropy-inspired entropy proxy in zero-shot NAS.

## Related Concepts

- [[Self-Supervised Learning]]
- [[Spearman's Rank Correlation]]

