---
type: concept
aliases: [Conv Padding, Padding in CNN]
---

# Convolutional Padding

## Intuition
Convolutional padding adds extra border pixels before convolution so feature maps keep useful spatial size and boundary information is handled in a controlled way.

## Why It Matters
Without padding, feature maps shrink quickly and boundary pixels are underused. With different padding modes, models can behave differently near image edges.

## Tiny Example
For a 3x3 kernel on a 32x32 image, no padding yields 30x30 output, while padding=1 keeps 32x32 output.

## Definition
Padding is a boundary extension operator applied to tensors before convolution. Common modes include zero-fill, reflection, replication, and circular wrap.

## Key Points
1. Padding mode changes boundary statistics seen by the model.
2. Same kernel and weights can produce different robustness under different padding modes.
3. Padding choice affects both accuracy and runtime.

## How This Paper Uses It
- [[Padding-Robustness Interplay]]: The paper treats padding mode and padding size as primary experimental variables for robustness analysis.

## Representative Papers
- [[On the Interplay of Convolutional Padding and Adversarial Robustness]]: Systematic robustness study across padding modes.

## Related Concepts
- [[Adversarial Robustness]]
- [[AutoAttack]]

