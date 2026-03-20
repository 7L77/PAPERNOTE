---
type: concept
aliases: ["Training-free NAS", "Zero-Cost NAS"]
---

# Zero-shot NAS

## Intuition

Zero-shot NAS means we try to compare candidate architectures before fully training them. Instead of spending hours or days training every model, we compute a cheap score at initialization and hope that score preserves the final ranking well enough to guide search.

## Why It Matters

It is one of the most direct ways to cut NAS cost. If the proxy is reliable, we can reject weak candidates early and reserve expensive training only for the few most promising ones.

## Tiny Example

Suppose we have 5,000 candidate CNNs. Multi-shot NAS would train many of them. Zero-shot NAS computes a score such as SNIP, Synflow, or Zen-score right after random initialization and keeps only the highest-ranked subset.

## Definition

Zero-shot NAS is a neural architecture search paradigm that replaces or heavily reduces candidate training during the search stage by using initialization-time proxies to rank architectures.

## Key Points

1. The main benefit is search-efficiency rather than guaranteed best final accuracy.
2. Its usefulness depends almost entirely on how well the chosen proxy correlates with trained performance.
3. It becomes especially attractive when architecture evaluation dominates the NAS budget.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: uses zero-shot NAS as the central object of study and compares when current proxies succeed or fail.

## Representative Papers

- [[Zero-shot NAS Survey]]: survey and large-scale evaluation of proxy behavior.
- [[Zero-Cost Proxies for Lightweight NAS]]: early influential zero-cost proxy paper.

## Related Concepts

- [[Zero-shot Proxy]]
- [[Hardware-aware NAS]]

