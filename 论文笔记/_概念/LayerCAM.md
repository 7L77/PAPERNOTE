---
type: concept
aliases: [Layer-wise CAM, LayerCAM Explanation]
---

# LayerCAM

## Intuition
LayerCAM visualizes which spatial regions support a prediction by weighting activation maps with positive gradients at each layer.

## Why It Matters
It helps diagnose what the model focuses on before and after perturbations, which is useful for robustness analysis.

## Tiny Example
If clean-image explanation highlights object center but adversarial-image explanation shifts to borders, the attack likely redirected model attention.

## Definition
LayerCAM is a class activation mapping method that computes pixel-level relevance from intermediate feature maps using gradient-based weights, enabling fine-grained visual explanations.

## Key Points
1. Works on intermediate layers, not only final convolution output.
2. Useful for comparing explanation shifts across conditions.
3. Explanations are diagnostic signals, not direct causal proofs.

## How This Paper Uses It
- [[Padding-Robustness Interplay]]: Uses LayerCAM shift maps to show padding-dependent migration of attention under successful attacks.

## Representative Papers
- [[LayerCAM]]: Exploring hierarchical class activation maps for localization.

## Related Concepts
- [[Adversarial Robustness]]
- [[Convolutional Padding]]

