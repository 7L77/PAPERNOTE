---
type: concept
aliases: [Shapley value, Cooperative game attribution]
---

# Shapley Value

## Intuition

When many components work together, Shapley Value asks a fair question: "on average, how much does one component help if we consider every possible order of joining the team?"

## Why It Matters

It gives a principled way to attribute contribution under interaction effects, where the value of one component depends on what other components are present.

## Tiny Example

Suppose three search primitives jointly give robustness gain `+9`, but individually none can reach that. Shapley Value averages each primitive's marginal gain across all insertion orders, so we do not over-credit a primitive that only works with a specific partner.

## Definition

For participant `i` in set `N`, with coalition-value function `v(S)`:

\[
\phi_i(v)=\sum_{S \subseteq N\setminus\{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!}\big(v(S\cup\{i\})-v(S)\big)
\]

This is the expected marginal contribution of `i` over all permutations.

## Key Points

1. Handles interaction and synergy better than single ablation.
2. Satisfies fairness axioms (efficiency, symmetry, dummy, additivity).
3. Exact computation is expensive (`O(2^N)` or permutation-form `O(N!)`), so sampling estimators are common.

## How This Paper Uses It

- [[LRNAS]] models each search primitive as a participant and defines coalition benefit as natural-accuracy gain plus adversarial-robustness gain (Sec. III-C, Eq. 3-8).
- It uses sampled permutations to build an unbiased estimator for practical search.

## Representative Papers

- L. S. Shapley, "A Value for n-Person Games," 1953.
- H. Xiao et al., "Shapley-NAS: Discovering Efficient and Robust Architectures via Shapley Value Guidance," 2022.

## Related Concepts

- [[Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Adversarial Robustness]]
