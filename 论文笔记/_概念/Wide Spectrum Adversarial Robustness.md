---
type: concept
aliases: [WSR, Wide-spectrum robustness]
---

# Wide Spectrum Adversarial Robustness

## Intuition

Robustness should not be judged at only one perturbation strength. A model is "wide-spectrum robust" if it stays robust across a broad range of attack strengths.

## Why It Matters

Real-world attacks do not come with one fixed \(\epsilon\). Single-strength optimization may look good on one benchmark point but fail at stronger or shifted attack magnitudes.

## Tiny Example

Model A is best at \(\epsilon=0.03\) but collapses at \(\epsilon=0.17\). Model B is slightly worse at 0.03 but consistently better from 0.06 to 0.25. Wide-spectrum robustness prefers Model B.

## Definition

A practical definition is average robust performance over a selected strength set:
\[
\text{AvgRobustAcc}=\frac{1}{K}\sum_{k=1}^K \text{Acc}(\epsilon_k).
\]

## Math Form (if needed)

Given strengths \(\{\epsilon_1,...,\epsilon_K\}\), evaluate model under each attack budget and aggregate by mean (or weighted mean) for search/training objectives.

## Key Points

1. It is a distributional view over attack strengths, not a single-point metric.
2. It emphasizes robustness stability across perturbation scales.
3. It usually requires better efficiency tricks to keep computation practical.

## How This Paper Uses It

- [[Wsr-NAS]]: Uses multi-strength losses in search objective and reports average robustness across \(\epsilon \in \{0.03,0.10,0.17,0.25\}\).

## Representative Papers

- [[Wsr-NAS]]: Explicitly formulates robust NAS for wide-strength coverage.

## Related Concepts

- [[Adversarial Robustness]]
- [[Robust Search Objective]]
- [[PGD Attack]]
- [[Adversarial Noise Estimator]]

