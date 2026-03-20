---
type: concept
aliases: [Empirical Fisher Pruning, Fisher-based Channel Pruning]
---

# Fisher Pruning

## Intuition

Instead of pruning a feature because its weights are small, Fisher pruning asks a more task-aware question: if this parameter or feature map disappears, how much will the model's loss increase?

## Why It Matters

That makes pruning decisions sensitive to what the model actually predicts, not just to magnitude heuristics. It is especially useful when we want real deployment speedups from channel removal.

## Tiny Example

Two channels can have similar average activation, but one may sharply affect the output saliency distribution while the other barely matters. Fisher pruning keeps the first and removes the second.

## Definition

Fisher pruning estimates the increase in loss from removing a parameter or feature map using a local second-order approximation whose curvature term is approximated by the empirical [[Fisher Information Matrix]].

## Math Form (if needed)

For a feature map or parameter `k`, a common score is:

`Delta_k ~= (1 / 2N) * sum_n g_nk^2`

where `g_nk` is the per-example gradient of the loss with respect to that prunable unit or its mask.

## Key Points

1. It is gradient-based and more task-sensitive than L1 magnitude pruning.
2. It is usually applied at channel / feature-map level when runtime matters.
3. It can be combined with a compute penalty to optimize speed-accuracy tradeoffs directly.

## How This Paper Uses It

- [[Faster gaze prediction with dense networks and Fisher pruning]]: Uses Fisher pruning to remove saliency-model feature maps while accounting for FLOPs reduction.

## Representative Papers

- [[Faster gaze prediction with dense networks and Fisher pruning]]: A principled empirical-Fisher derivation for gaze-model pruning.
- Molchanov et al. (ICLR 2017): Closely related gradient-based pruning for CNNs.

## Related Concepts

- [[Fisher Information Matrix]]
- [[Knowledge Distillation]]
- [[Saliency Prediction]]

