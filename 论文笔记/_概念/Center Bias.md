---
type: concept
aliases: [Central Fixation Bias, Image Center Prior]
---

# Center Bias

## Intuition

Humans tend to look near the image center more often than near the borders, even before considering image content.

## Why It Matters

If a saliency model ignores this prior, it can underperform even when its visual features are strong, because many fixation benchmarks contain a strong center tendency.

## Tiny Example

Two identical objects placed at the center and near the edge often do not receive equal fixation probability in real eye-tracking data; the centered one usually attracts more looks.

## Definition

Center bias is a dataset-level prior over fixation locations that captures the tendency of observers to fixate near the image center.

## Math Form (if needed)

It is often added as a prior term such as `log Q(x, y)` before normalization of the final saliency distribution.

## Key Points

1. It is not purely a model artifact; it is also present in human data collection setups.
2. The strength of the prior can differ across datasets.
3. Good saliency models usually combine content-driven evidence with this prior.

## How This Paper Uses It

- [[Faster gaze prediction with dense networks and Fisher pruning]]: Adds a dataset-dependent log-probability center prior before the final softmax.

## Representative Papers

- DeepGaze-style models often include center-bias terms explicitly.
- [[Faster gaze prediction with dense networks and Fisher pruning]]: Retains the center-bias prior while compressing the rest of the saliency model.

## Related Concepts

- [[Saliency Prediction]]
- [[KL Divergence]]

