---
type: concept
aliases: [AN-Estimator, ANE]
---

# Adversarial Noise Estimator

## Intuition

Instead of running a full PGD attack for every target perturbation strength, train a lightweight module that can "interpolate/extrapolate" adversarial noises from a few already-generated strengths.

## Why It Matters

In robust NAS, generating many adversarial validation sets is often the dominant cost. AN-Estimator lets us scale to more strengths with much lower compute.

## Tiny Example

If we already have PGD noises at \(\epsilon=0.03,0.06,0.09\), AN-Estimator can generate approximations for \(\epsilon=0.045,0.075,0.105\) without rerunning full PGD each time.

## Definition

An Adversarial Noise Estimator is a parametric function
\[
\hat{\delta}_{\hat{\epsilon}}=\Phi(x,\delta_{\epsilon_1},...,\delta_{\epsilon_{N_1}},\hat{\epsilon})
\]
that predicts adversarial noise at target strength \(\hat{\epsilon}\) from input \(x\) and source noises at known strengths.

## Math Form (if needed)

Training objective in Wsr-NAS uses MSE:
\[
\mathcal{L}_a(\Phi)=\frac{1}{T_a}\sum_{t=1}^{T_a}\|\Phi(\cdot)-\delta_t^{\hat{\epsilon}}\|_2^2
\]
where \(T_a\) is memory size and \(\delta_t^{\hat{\epsilon}}\) is target noise label.

## Key Points

1. It trades exactness for speed to support multi-strength robust search.
2. Quality depends on estimator architecture and training memory freshness.
3. It is most useful when paired with exact base-strength attacks.

## How This Paper Uses It

- [[Wsr-NAS]]: Uses AN-Estimator to expand adversarial strengths during search while keeping runtime manageable.

## Representative Papers

- [[Wsr-NAS]]: Introduces AN-Estimator for wide-spectrum robust NAS.

## Related Concepts

- [[Wide Spectrum Adversarial Robustness]]
- [[Validation Loss Estimator]]
- [[PGD Attack]]
- [[Adversarial Robustness]]

