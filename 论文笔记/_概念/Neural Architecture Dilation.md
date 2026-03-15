---
type: concept
aliases: [Architecture Dilation, NAD]
---

# Neural Architecture Dilation

## Intuition

Neural Architecture Dilation means we do not redesign an entire network from scratch.  
Instead, we keep a strong backbone and add extra architecture modules in parallel/attached form, so capacity and robustness can increase with smaller disruption to existing clean accuracy.

## Why It Matters

In adversarial robustness, full robust NAS can be expensive and unstable. Dilation-style design gives a practical middle ground: keep what already works on clean data, and only optimize a small additive branch for robustness.

## Tiny Example

Suppose a WRN backbone classifies clean CIFAR-10 images well but fails under PGD attacks.  
With architecture dilation, each backbone block gets an extra searchable cell. The final feature is `backbone_feature + dilation_feature`, so the added branch learns robust cues while the backbone retains clean semantics.

## Definition

Neural Architecture Dilation is an architecture augmentation strategy that maps a base model `f_b` to a hybrid model `f_hyb = f_b + f_d`, where `f_d` is a learned/searchable dilation branch attached block-wise (or stage-wise) to the backbone, usually under constraints such as standard performance preservation and compute budget.

## Math Form (if needed)

A representative form (used by NADAR) is:

`z_hyb^(l) = f_b^(l)(z_hyb^(l-1)) + f_d^(l)(z_hyb^(l-1), z_hyb^(l-2))`

- `f_b^(l)`: block `l` of the backbone.
- `f_d^(l)`: dilation cell attached to block `l`.
- `z_hyb^(l)`: fused latent representation at block `l`.

This equation shows dilation as additive feature expansion, not backbone replacement.

## Key Points

1. Dilation is incremental architecture design, not full architecture replacement.
2. It is especially useful when clean accuracy of the backbone should be preserved.
3. Constraints (standard loss / FLOPs) are usually necessary to avoid overgrowth.

## How This Paper Uses It

- [[NADAR]]: attaches one NAS cell to each backbone block and optimizes the dilation branch for adversarial robustness with standard-loss and FLOPs constraints.

## Representative Papers

- [[NADAR]]: formalizes architecture dilation for adversarial robustness with constrained optimization.

## Related Concepts

- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Adversarial Robustness]]
