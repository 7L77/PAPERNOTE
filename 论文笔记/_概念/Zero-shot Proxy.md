---
type: concept
aliases: ["Zero-cost Proxy", "Training-free Proxy"]
---

# Zero-shot Proxy

## Intuition

A zero-shot proxy is the cheap score that stands in for actual trained accuracy. It is the thermometer of zero-shot NAS: we do not observe the true quantity directly, so we use a fast surrogate and hope it tracks what we care about.

## Why It Matters

Without a useful proxy, zero-shot NAS collapses. The whole pipeline only works if the proxy ranking is close enough to the ranking after real training.

## Tiny Example

If two architectures are compared with SNIP at initialization and SNIP gives model A a much higher score than model B, then the search algorithm will usually prefer A without training either model.

## Definition

A zero-shot proxy is a computation-efficient statistic of an untrained or randomly initialized neural network used to estimate or rank its eventual trained performance.

## Key Points

1. A proxy is valuable only through its rank quality, not through its absolute numeric scale.
2. Different proxies emphasize different properties such as trainability, expressivity, or generalization.
3. A proxy that looks good on all architectures may still fail on the top-performing tail that NAS actually cares about.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: categorizes proxies, compares them across benchmarks, and shows where they fail against `#Params/#FLOPs`.

## Representative Papers

- [[Zero-shot NAS Survey]]: broad comparison across tasks and hardware constraints.
- [[Zen-NAS]]: example of a proxy designed around expressivity at initialization.

## Related Concepts

- [[Zero-shot NAS]]
- [[Trainability]]

