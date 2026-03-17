---
type: concept
aliases: [Feature Collinearity, Activation Collinearity]
---

# Feature Map Collinearity

## Intuition
Feature map collinearity means different channels carry highly overlapping directions/information. Instead of diverse responses, many channels become near-linear combinations of each other.

## Why It Matters
High collinearity often implies low effective diversity, weaker conditioning, and less robust optimization behavior.

## Tiny Example
If 32 channels in a block mostly detect the same edge pattern with only small scale differences, channel space is highly collinear and little new information is added.

## Definition
Given layer feature matrix \(X_\phi\) (channels reshaped as vectors), collinearity is high when singular spectrum is highly skewed and condition number is large.

## Math Form (if needed)
- High collinearity \(\Rightarrow \sigma_{\min}(X_\phi)\) small, \(c(X_\phi)=\sigma_{\max}/\sigma_{\min}\) large.
- A common diversity proxy is inverse condition signal \(\sigma_{\min}/\sigma_{\max}\).

## Key Points
1. Collinearity is a geometry-level redundancy notion.
2. It can be measured without labels from one forward pass.
3. Lower collinearity generally means richer channel diversity.

## How This Paper Uses It
- [[Dextr]]: treats lower feature-map collinearity as beneficial for convergence/generalization; implements this via inverse condition signals.

## Representative Papers
- [[Dextr]]: explicitly links feature collinearity to C/G behavior in zero-shot NAS.

## Related Concepts
- [[Condition Number]]
- [[Singular Value Decomposition]]
- [[Gram Matrix]]

