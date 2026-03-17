---
type: concept
aliases: [Activation Search]
---

# Activation Function Search

## Intuition
Activation function search treats activation type as a searchable architectural choice, not a fixed default.

## Why It Matters
Different tasks/backbones may prefer different nonlinearities. Locking to ReLU can miss better candidates.

## Tiny Example
On one benchmark, GELU may outperform ReLU in a transformer-like backbone, while another CNN may still prefer ReLU or LeakyReLU.

## Definition
Activation function search explores candidate activation operators (e.g., ReLU, GELU, SiLU, ELU) within a model or search space and selects those yielding better target performance.

## Key Points
1. Extends NAS design space beyond topology/operators.
2. Training-free proxies may fail when they assume specific activation behavior.
3. Good search methods should remain effective across non-ReLU candidates.

## How This Paper Uses It
- [[RBFleX-NAS]] introduces NAFBee benchmark (VGG-19 and BERT variants with multiple activations).
- Shows that RBFleX-NAS can identify best-performing activation choices more reliably than several baselines.

## Representative Papers
- [[RBFleX-NAS]]

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Radial Basis Function Kernel]]

