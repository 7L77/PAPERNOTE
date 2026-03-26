---
title: "Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective"
method_name: "TE-NAS"
authors: [Wuyang Chen, Xinyu Gong, Zhangyang Wang]
year: 2021
venue: ICLR
tags: [nas, training-free-nas, ntk, linear-regions, iclr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2102.11535
local_pdf: D:/PRO/essays/papers/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective.pdf
local_code: D:/PRO/essays/code_depots/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective
created: 2026-03-26
---

# Paper Note: TE-NAS

## Metadata
| Item | Value |
|---|---|
| Paper | Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective |
| Authors | Wuyang Chen, Xinyu Gong, Zhangyang Wang |
| Venue | ICLR 2021 |
| arXiv | https://arxiv.org/abs/2102.11535 |
| HTML | https://arxiv.org/html/2102.11535 |
| Code | https://github.com/VITA-Group/TENAS |
| Local PDF | `D:/PRO/essays/papers/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective.pdf` |
| Local code | `D:/PRO/essays/code_depots/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective` |

## One-line summary
> TE-NAS is a training-free NAS framework that ranks candidate operators by combining changes in [[Neural Tangent Kernel]] [[Condition Number]] and [[Linear Regions]], then prunes low-importance operators edge-by-edge.

## Core contributions
1. Introduces a theory-inspired, label-free architecture quality signal using two indicators: NTK condition number and number of linear regions (Sec. 3.1).
2. Proposes a pruning-by-importance search algorithm instead of pure sample-and-evaluate loops, reducing complexity from roughly `|O|^E`-style sampling burden to iterative operator elimination (Sec. 3.2, Algorithm 1).
3. Shows strong empirical performance-cost tradeoff on NAS-Bench-201 and DARTS, with very low search cost (Table 1-3).

## Problem setting and motivation
- Target task: [[Training-free NAS]] in [[Cell-based Search Space]].
- Pain point: prior NAS methods either train heavy supernets or rely on truncated training that introduces bias.
- TE-NAS hypothesis: architecture trainability and expressivity can be approximated at initialization and can guide search without full training.

## Method details

### 1) Trainability proxy: NTK condition number
- Define finite-width NTK `\hat{\Theta}(x,x') = J(x)J(x')^T`.
- Use condition number as trainability metric:

$$
\kappa_N = \frac{\lambda_{\max}}{\lambda_{\min}}
$$

- Lower `\kappa_N` indicates better trainability.
- Empirical correlation: Figure 1 reports Kendall-tau `-0.42` on CIFAR-100 in NAS-Bench-201.

### 2) Expressivity proxy: number of linear regions
- For ReLU networks, count distinct activation patterns / linear regions.
- Paper uses repeated random initialization and averages region counts:

$$
\hat{R}_N \approx \mathbb{E}_{\theta}[R_{N,\theta}]
$$

- Higher `\hat{R}_N` indicates stronger expressivity.
- Empirical correlation: Figure 3 reports Kendall-tau `0.50`.

### 3) Joint ranking + pruning-by-importance
- For each candidate operator removal, TE-NAS evaluates:
  - NTK change tendency (remove ops that reduce `\kappa_N` more strongly).
  - Linear-region change tendency (remove ops that hurt expressivity less).
- Assign ranking indices separately, then combine via rank-sum score:

$$
s(o_j) = s_{\kappa}(o_j) + s_R(o_j)
$$

- On each edge, prune the operator with lowest importance score each round until single-path (Algorithm 1).
- I use the concept link [[Pruning-by-Importance NAS]] for this search pattern.

## Key equations and what they mean
1. Eq. (1): Infinite-width training dynamics approximation.
2. Eq. (2): Per-eigenmode convergence relation.
3. Eq. (3): `\kappa_N` as NTK conditioning metric for trainability.
4. Eq. (4): Linear-region definition from activation patterns.
5. Eq. (5): Monte-Carlo style estimate of expected linear-region count.

## Important figures and tables

### Figures
- Fig. 1: `\kappa_N` vs test accuracy, negative correlation (Kendall-tau `-0.42`).
- Fig. 3: `\hat{R}_N` vs test accuracy, positive correlation (Kendall-tau `0.50`).
- Fig. 4: operator preference mismatch between trainability and expressivity objectives.
- Fig. 5: pruning trajectory shows early stage rapid trainability improvement, then expressivity-preserving refinement.
- Fig. 8: in DARTS, shallow/wide structures are favored by both indicators.
- Fig. 9: rank combination improves correlation (Kendall-tau `-0.64`).
- Fig. 10: train accuracy strongly correlates with test accuracy in NAS-Bench-201 (Kendall-tau `0.79`).

### Table 1 (NAS-Bench-201)
- TE-NAS: CIFAR-10 `93.9±0.47`, CIFAR-100 `71.24±0.56`, ImageNet16-120 `42.38±0.46`.
- Search cost: `1558` GPU-sec, much lower than many gradient-based baselines.

### Table 2 (DARTS, CIFAR-10)
- TE-NAS test error `2.63±0.064%`, params `3.8M`, search cost `0.05` GPU-day.

### Table 3 (DARTS, ImageNet mobile setting)
- When searched on ImageNet: top-1/top-5 error `24.5%/7.5%`, params `5.4M`, cost `0.17` GPU-day.

### Table 4 (Ablation: single indicator)
- Only `\kappa_N`: `69.25±1.29` on CIFAR-100.
- Only `\hat{R}_N`: `70.48±0.29`.
- Full TE-NAS: `71.24±0.56`.

### Table 5 (Ablation: combination strategy)
- Rank-sum combination outperforms min/max/direct-delta combinations.

## Implementation details from paper appendix
- NTK uses one mini-batch of size 32.
- Linear regions use 5000 images.
- Both indicators repeated 3 times with Kaiming initialization.
- Retraining follows common DARTS-style settings (cutout, drop-path, auxiliary tower for CIFAR-10; label smoothing for ImageNet).

## Code alignment notes (archived repo)
- Search entry: `prune_tenas.py`.
- NTK computation: `lib/procedures/ntk.py` (`get_ntk_n`, eigenvalue ratio for condition number).
- Linear-region counting: `lib/procedures/linear_region_counter.py` (hook ReLU activations, count unique sign patterns).
- Rank-based pruning logic: `prune_func_rank` in `prune_tenas.py`.
- Practical implementation computes per-operator relative change in NTK/regions under operator removal, then rank-sums those deltas.

## Critical view
### Strengths
1. Very strong efficiency while keeping competitive quality.
2. Method is interpretable: trainability vs expressivity tradeoff is explicit.
3. Provides a reusable training-free pruning template beyond this paper.

### Limitations
1. Correlation quality can depend on search space/task; no universal guarantee.
2. Proxy computation is still non-trivial for large models/search spaces.
3. Theoretical link is suggestive, but final test accuracy depends on retraining/generalization dynamics beyond initialization proxies.

## Related notes and concepts
- [[TE-NAS]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
- [[Neural Tangent Kernel]]
- [[Condition Number]]
- [[Linear Regions]]
- [[Kendall's Tau]]
- [[NAS-Bench-201]]
- [[Differentiable Architecture Search]]
- [[Pruning-by-Importance NAS]]
