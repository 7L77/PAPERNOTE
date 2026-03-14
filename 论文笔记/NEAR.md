---
title: "NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance"
method_name: "NEAR"
authors: [Raphael T. Husistein, Markus Reiher, Marco Eckhoff]
year: 2025
venue: ICLR
tags: [nas, training-free-nas, zero-cost-proxy, effective-rank, iclr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2408.08776
local_pdf: D:/PRO/essays/papers/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance.pdf
local_code: D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance
created: 2026-03-14
---

# Paper Note: NEAR

## Basic Info
| Item | Value |
|---|---|
| Paper | NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance |
| arXiv | https://arxiv.org/abs/2408.08776 |
| Venue | ICLR 2025 |
| Code | https://github.com/ReiherGroup/NEAR |
| Local PDF | `D:/PRO/essays/papers/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance.pdf` |
| Local code | `D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance` |

## One-line Summary
> NEAR uses the [[Effective Rank]] of layer-wise pre/post activations to estimate model quality without training, and works as a robust [[Zero-Cost Proxy]] across multiple NAS spaces.

## Core Contributions
1. Proposes NEAR, a training-free proxy based on effective-rank geometry of activations.
2. Shows broad correlation with final accuracy on NATS-Bench-TSS/SSS and NAS-Bench-101.
3. Extends usage beyond architecture ranking: layer-size estimation in MLPs and guidance for activation/initialization choices.

## Problem and Motivation
- Existing proxies often depend on specific activations (especially ReLU), labels, or narrow search-space behavior.
- Some proxies do not consistently beat trivial baselines like `#Params`.
- The paper targets a more activation-agnostic and broadly stable proxy.

## Method Details
### 1) Effective Rank as Expressivity Signal
For matrix `A`, NEAR uses:
\[
\mathrm{erank}(A)=\exp(H(p_1,\dots,p_Q)),\quad
H=-\sum_{k=1}^{Q} p_k \log p_k,\quad
p_k=\frac{\sigma_k}{\sum_i \sigma_i}
\]
where `\sigma_k` are singular values.  
Interpretation: higher effective rank implies less collapsed/more balanced feature geometry.

### 2) NEAR Score
For network layers `l=1..L`, define pre-activation matrix `Z_l` and post-activation matrix `H_l`, then:
\[
s_{\mathrm{NEAR}}=\sum_{l=1}^{L}\left(\mathrm{erank}(Z_l)+\mathrm{erank}(H_l)\right)
\]
Higher score indicates better expected performance.  
Paper reports averaging over repeated random draws (e.g., 32 repetitions on NAS benchmarks).

### 3) CNN Adaptation
- Convolution outputs are reshaped to matrices before rank calculation.
- A submatrix sampling strategy is used to reduce computation while retaining trend consistency.

### 4) Layer-size Estimation
- Empirically fits a power law to relative NEAR score vs. layer size.
- Chooses size where slope falls below a threshold, giving a practical parameter-efficiency tradeoff.

## Key Results
### Correlation on NAS benchmarks
- NATS-Bench-TSS (Kendall/Spearman):
1. CIFAR-10: `0.70 / 0.88`
2. CIFAR-100: `0.69 / 0.87`
3. ImageNet16-120: `0.66 / 0.84`
- NATS-Bench-SSS:
1. CIFAR-10: `0.74 / 0.91`
2. CIFAR-100: `0.62 / 0.82`
3. ImageNet16-120: `0.76 / 0.92`
- NAS-Bench-101:
1. CIFAR-10: `0.52 / 0.70`

### Overall ranking quality
- Average rank across spaces/datasets (lower is better):
1. NEAR: `1.71`
2. MeCoopt: `2.57`
3. ZiCo: `3.57`

### Hyperparameter selection signals
- On provided experiments, NEAR can identify clearly poor activation/init combinations (e.g., Tanhshrink cases).
- For very close candidates, NEAR ordering may not always match tiny final-loss gaps.

## Paper-Implementation Alignment
- `src/near_score/near_score.py` computes effective rank via SVD singular values + entropy, aligned with Eq. (4)-(5).
- `__get_near_score(...)` aggregates layer outputs and sums effective ranks, matching the paper's score form.
- Conv outputs are reshaped and subsampled in code, consistent with the efficiency argument in Sec. 3.3.
- `estimate_layer_size(...)` fits a power function and uses `slope_threshold`, matching Sec. 4.2 intuition.

## Critical Takeaways
### Strengths
1. Label-free and activation-flexible proxy design.
2. Strong cross-space ranking consistency, not just one benchmark.
3. Practical extension to architecture-adjacent decisions (size, init, activation).

### Limitations
1. Proxy measures expressivity, not full optimization dynamics.
2. Fine-grained differences among top candidates may be unresolved.
3. Some improvements are task/search-space dependent.

## Reproducibility Notes
- [x] Official code released
- [x] Local PDF archived
- [x] Local code archived
- [ ] Full benchmark rerun done locally

## Related Concepts
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
- [[Network Expressivity]]
- [[Effective Rank]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]

