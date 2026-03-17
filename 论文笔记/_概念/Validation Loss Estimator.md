---
type: concept
aliases: [VLE, Loss Predictor for NAS]
---

# Validation Loss Estimator

## Intuition

Instead of evaluating each candidate architecture on all validation conditions directly, train a small predictor to estimate those validation losses from architecture representation.

## Why It Matters

Architecture updates in robust NAS can be expensive because each update may require many adversarial validation passes. A good estimator makes architecture optimization much cheaper.

## Tiny Example

For one architecture, evaluating clean + 6 adversarial strengths directly may take many forward/backward passes. A trained VLE predicts these 7 losses in one lightweight predictor forward pass.

## Definition

A Validation Loss Estimator is a learned function
\[
\hat{L}=\Psi(H)
\]
that maps architecture encoding \(H\) to a vector of predicted validation losses over multiple conditions.

## Math Form (if needed)

In Wsr-NAS:
\[
\hat{L}=\{\hat{L}_{natural},\hat{L}_{\epsilon_1},...,\hat{L}_{\epsilon_{N_1+N_2}}\}
\]
and training minimizes
\[
\mathcal{L}_v(\Psi)=\frac{1}{T}\sum_{t=1}^{T}\|\Psi(H_t)-L_t\|_2^2.
\]

## Key Points

1. It is a surrogate model for validation loss landscape.
2. Memory design (\(M_v\)) is crucial to keep estimator aligned with evolving supernet.
3. Predictor quality directly affects architecture update quality.

## How This Paper Uses It

- [[Wsr-NAS]]: VLE is the core of EWSS; it predicts clean and multi-strength robust losses used for architecture optimization.

## Representative Papers

- [[Wsr-NAS]]: Uses RNN-based VLE with multi-head outputs in robust NAS.

## Related Concepts

- [[Robust Search Objective]]
- [[One-shot NAS]]
- [[Super-network]]
- [[Adversarial Noise Estimator]]

