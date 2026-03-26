---
type: concept
aliases: [Hebb Rule, Cells that fire together wire together]
---

# Hebbian Learning

## Intuition
Neurons that activate together strengthen their connection.

## Why It Matters
Hebbian updates are local and biologically plausible, avoiding full-gradient global credit assignment.

## Tiny Example
If input feature `x_i` and output activation `y_j` are both high, weight `w_ij` gets increased by a local co-activation term.

## Definition
Hebbian learning updates synapses using local activity statistics, often proportional to a pre/post-neuron correlation term such as `delta w_ij ∝ x_i * y_j`.

## Key Points
1. Locality makes it biologically appealing.
2. Pure Hebbian updates may require normalization/stabilization.
3. Modern variants can scale beyond toy settings with additional mechanisms.

## How This Paper Uses It
- [[BioNAS]] includes a Hebbian-inspired convolution option in search-space extensions, demonstrating framework flexibility even when this option is not the top performer.

## Representative Papers
- Hebbian CNN scaling works cited in BioNAS references [1, 29].
- [[BioNAS]] for mixed-rule NAS integration.

## Related Concepts
- [[Feedback Alignment]]
- [[Predictive Coding]]
- [[Adversarial Robustness]]

