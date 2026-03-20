---
type: concept
aliases: [Visual Saliency Prediction, Fixation Prediction, Gaze Prediction]
---

# Saliency Prediction

## Intuition

Given an image, saliency prediction estimates where humans are likely to look.

## Why It Matters

It turns human visual attention into a machine-usable signal for cropping, compression, interface design, perception studies, and downstream vision systems.

## Tiny Example

In a street image, a saliency model should assign high probability to faces, text signs, or the only moving-looking object instead of spreading attention uniformly.

## Definition

Saliency prediction models the probability distribution of human fixations over image pixels, often using eye-tracking data as supervision.

## Math Form (if needed)

A common output is a normalized map `Q(x, y | I)` over pixel locations, where higher probability means a human observer is more likely to fixate there.

## Key Points

1. Modern saliency models often output probability maps rather than binary masks.
2. Evaluation uses metrics such as AUC, NSS, SIM, KL, and related fixation-benchmark scores.
3. Dataset priors such as [[Center Bias]] often matter a lot.

## How This Paper Uses It

- [[Faster gaze prediction with dense networks and Fisher pruning]]: Predicts fixation distributions from images and compresses the saliency network for faster inference.

## Representative Papers

- DeepGaze I / II: Strong deep saliency baselines built on object-recognition features.
- [[Faster gaze prediction with dense networks and Fisher pruning]]: Efficient saliency modeling with distillation and pruning.

## Related Concepts

- [[Center Bias]]
- [[Knowledge Distillation]]
- [[KL Divergence]]

