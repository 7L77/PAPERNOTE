---
type: concept
aliases: [SynFlow, Synaptic Saliency Flow]
---

# Synaptic Flow

## Intuition
Synaptic Flow is a data-free proxy score that estimates how much each parameter contributes to signal propagation in a network at initialization.

## Why It Matters
In NAS, it can rank many architectures cheaply without full training, which is useful when search budget is tight.

## Tiny Example
If two candidate architectures have similar FLOPs but one has much stronger SynFlow score, NAS may prioritize that architecture for further evaluation.

## Definition
SynFlow computes parameter saliency by using a synthetic all-ones input and a positive-weight reparameterization, then aggregates saliency over all parameters as the architecture score.

## Math Form (if needed)
The paper uses the common form:
\[
\text{SynFlow}(w) = \left| \frac{\partial L}{\partial w} \odot w \right|,
\]
where \(L\) is a synthetic loss and \(\odot\) is element-wise product.

## Key Points
1. It is training-free and can be computed before learning starts.
2. It is often used as a ranking proxy, not a direct accuracy predictor.
3. Strong SynFlow score does not always guarantee best adversarial robustness.

## How This Paper Uses It
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Uses SynFlow as the training-free objective in both GA and NSGA-II variants.

## Representative Papers
- [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]: Evaluates SynFlow under adversarial-training-aware robustness criteria.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]

