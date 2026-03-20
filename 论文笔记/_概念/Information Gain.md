---
type: concept
aliases: [IG, Mutual Information Gain]
---

# Information Gain

## Intuition
Information Gain (IG) measures how much uncertainty about a target is reduced after revealing an extra variable.

## Why It Matters
When combining multiple NAS proxies, we need to know whether a new proxy adds genuinely new signal or only repeats existing information.

## Tiny Example
Suppose proxy `z1` already tells us architecture ranking pretty well. If adding `z2` barely changes uncertainty on validation accuracy, `IG(z2)` is low, meaning `z2` is mostly redundant to `z1`.

## Definition
Given target random variable `y` and proxy variables `z_i, z_j`, one common conditional IG form is:
\[
IG(z_j)=H(y|z_i)-H(y|z_i,z_j)
\]
where `H(.)` is entropy. Larger reduction means `z_j` contributes more additional information beyond `z_i`.

## Key Points
1. IG is conditional and depends on what information is already known.
2. Low IG can mean redundancy; high IG can mean complementarity.
3. In practice, estimator choice and sample size can change IG stability.

## How This Paper Uses It
- [[L-SWAG]]: In LIBRA, the second proxy is chosen by minimum IG among high-correlation candidates (Sec. 3.2, Eq. 9), as a heuristic for robust proxy pairing.

## Representative Papers
- [[ZCP-Eval]]: Uses multiple proxy statistics and ranking analysis to study proxy behavior across settings.
- [[L-SWAG]]: Uses IG inside a concrete proxy selection algorithm (LIBRA).

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Proxy Voting]]
