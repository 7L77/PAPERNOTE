---
type: concept
aliases: [Partial Feedback Decision Game, PM Game]
---

# Partial Monitoring

## Intuition

Partial monitoring is an online decision setting where you never observe reward directly in full detail. You only get indirect feedback and must still learn good actions over time.

## Why It Matters

Many real systems provide incomplete feedback. You can choose an action and get some observation, but that observation is only partially informative about the true objective.

## Tiny Example

Imagine choosing ad creatives where you only observe clicks from shown ads, not true user preference over all options. You must learn from partial signals.

## Definition

A learner repeatedly:
1. chooses an action,
2. receives observation feedback,
3. incurs reward/loss that is not fully revealed.

The goal is to minimize cumulative regret under partial feedback.

## Math Form (if needed)

Typical analysis defines regret:
\[
\mathrm{Reg}_t=\sum_{\tau=1}^{t}\left(r(a^*)-r(a_\tau)\right)
\]
where \(a^*\) is the best fixed action and \(r(\cdot)\) is expected reward. In partial monitoring, reward differences are inferred indirectly from observations.

## Key Points

1. Feedback is weaker than full-information settings.
2. Observability conditions determine learnability and regret rates.
3. It provides a theoretical lens for BO-style search with indirect reward signals.

## How This Paper Uses It

- [[RoBoT]]: maps weight-vector selection to partial monitoring and derives expected ranking bounds through regret analysis.

## Representative Papers

- [[RoBoT]]: applies partial-monitoring framing to training-free NAS metric ensembling.

## Related Concepts

- [[Bayesian Optimization]]
- [[Information Directed Sampling]]
