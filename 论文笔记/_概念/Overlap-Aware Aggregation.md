---
type: concept
aliases: ["Mask-aware Aggregation", "Sparse Parameter Aggregation"]
---

# Overlap-Aware Aggregation

## Intuition

In supernet federated training, different clients update different parameter subsets. Overlap-aware aggregation averages only over clients that actually touched each parameter.

## Why It Matters

If we naively average all updates, parameters that were not active in many sampled subnets get diluted or distorted, harming shared-weight quality.

## Tiny Example

Suppose parameter \(\theta_i\) appears in only 2 of 8 client subnets in one round. Overlap-aware aggregation averages \(\theta_i\) over those 2 valid updates, not all 8.

## Definition

Overlap-aware aggregation is a masked federated aggregation rule that accounts for per-parameter activation overlap across sampled subnets when updating supernet weights.

## Math Form (if needed)

Let \(I_k(\theta)\in\{0,1\}\) indicate whether client \(k\)'s subnet activates parameter \(\theta\). Then update terms are normalized by active-count-weighted masks rather than full client count.

## Key Points

1. It is essential for sparse, subnet-specific updates in weight-sharing supernets.
2. It prevents inactive parameters from being incorrectly averaged as zero-contribution.
3. It improves stability when client subnets are highly diverse.

## How This Paper Uses It

- [[DeepFedNAS]]: uses overlap-aware MaxNet-style aggregation with binary masks (Eq. 2, Alg. 1).

## Representative Papers

- [[DeepFedNAS]]: explicit overlap-aware aggregation in Pareto-guided federated supernet training.
- [[SuperFedNAS]]: baseline source of the federated supernet aggregation paradigm.

## Related Concepts

- [[Super-network]]
- [[Parameter Sharing in NAS]]
- [[Federated Neural Architecture Search]]

