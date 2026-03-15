---
type: concept
aliases: [Supernet, One-shot Supernet]
---

# Super-network

## Intuition
A super-network is an over-parameterized network that contains many candidate subnetworks. Train once, then sample many architectures.

## Why It Matters
It makes NAS practical by avoiding full retraining for every candidate architecture.

## Tiny Example
One layer has three operator options. In a super-network, these options share training context, and each path can be evaluated as a subnetwork.

## Definition
A super-network is a unified graph parameterization that encodes a search space of candidate architectures with shared weights.

## Key Points
1. It is the backbone of one-shot NAS.
2. Weight sharing reduces search cost but may introduce ranking bias.
3. Subnetwork extraction is needed for deployment.

## How This Paper Uses It
- [[LLaMA-NAS]]: Builds a mixed-rank adapter super-network and searches subnetworks via NSGA-II.

## Representative Papers
- [[LLaMA-NAS]]: Uses super-network to amortize adapter architecture training cost.

## Related Concepts
- [[One-shot NAS]]
- [[Mixed-Rank Adapter]]
