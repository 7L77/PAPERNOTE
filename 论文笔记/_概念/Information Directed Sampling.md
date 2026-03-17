---
type: concept
aliases: [IDS, Information-Directed Exploration]
---

# Information Directed Sampling

## Intuition

Information Directed Sampling (IDS) chooses actions that trade off immediate regret and information gain, instead of only chasing high predicted reward.

## Why It Matters

In expensive search, you want each query to both perform well and teach you something useful about uncertain regions.

## Tiny Example

If two weight vectors look similar in expected score, IDS may prefer the one that best reduces uncertainty about which region is globally better.

## Definition

IDS is a sequential decision strategy that selects actions by minimizing an information ratio, balancing:
- expected instantaneous regret,
- expected information gain about the optimal action.

## Math Form (if needed)

A common form uses:
\[
\Psi_t(a)=\frac{\Delta_t(a)^2}{g_t(a)}
\]
where:
- \(\Delta_t(a)\): expected regret of action \(a\),
- \(g_t(a)\): information gain from action \(a\).

Action minimizing \(\Psi_t\) is selected.

## Key Points

1. IDS is an explore-exploit principle based on information efficiency.
2. It can give strong regret guarantees in some partial-information settings.
3. It is conceptually different from plain UCB even when both are BO-style strategies.

## How This Paper Uses It

- [[RoBoT]]: theoretical section discusses IDS-style BO conditions to support bounded regret analysis.

## Representative Papers

- [[RoBoT]]: references IDS-style assumptions in its partial-monitoring-based proof setup.

## Related Concepts

- [[Bayesian Optimization]]
- [[Partial Monitoring]]
