---
type: concept
aliases: [Prediction Stability Under Attack]
---

# Stable Accuracy

## Intuition
Stable Accuracy asks a stricter question than normal robust accuracy: after perturbation, does the model keep the same prediction as before attack.

## Why It Matters
For adversarial robustness analysis, it separates "still correct by chance" from "truly prediction-stable", and often tracks robustness trends better than clean accuracy.

## Tiny Example
If a clean image is predicted as class A, and after attack the model still predicts A, this sample is stable.  
If prediction changes from A to B, it is unstable, even if one of them could still be correct in other settings.

## Definition
Given validation set `D`, model `f`, and attacked sample `x_hat`, Stable Accuracy is
the fraction of samples whose prediction is unchanged:
`|{x in D : f(x) = f(x_hat)}| / |D|`.

## Math Form (if needed)
\[
\text{StableAcc}=\frac{\left|\{x \in D:\ f(x)=f(\hat{x})\}\right|}{|D|}
\]

## Key Points
1. It measures prediction invariance under perturbation, not only correctness.
2. It is useful for diagnosing robustness mechanisms during training.
3. It can reveal behavior that clean accuracy or single attack accuracy alone misses.

## How This Paper Uses It
- [[NARes]]: Logs stable accuracy per epoch and in final evaluations, then analyzes its correlation with robust accuracy at architecture-space scale.

## Representative Papers
- [[NARes]]: Uses Stable Accuracy as a core diagnostic for robust architecture statistics.
- Wu et al. (2021): Discusses stability-oriented perspectives under adversarial training.

## Related Concepts
- [[Adversarial Robustness]]
- [[PGD Attack]]
- [[Lipschitz Constant]]

