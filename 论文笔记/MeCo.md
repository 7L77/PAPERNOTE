---
title: "MeCo: Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation"
method_name: "MeCo"
authors: [Tangyu Jiang, Haodi Wang, Rongfang Bie]
year: 2023
venue: NeurIPS
tags: [nas, training-free-nas, zero-cost-proxy, correlation]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=KFm2lZiI7n
local_pdf: D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation Supplementary Material.pdf
local_code: D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation
created: 2026-03-14
---

# Paper Note: MeCo

## Meta
| Item | Content |
|---|---|
| Paper | MeCo: Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation |
| NeurIPS page | https://proceedings.neurips.cc/paper_files/paper/2023/hash/95a50c26d63cf9f3dcf67784f40eb6fd-Abstract-Conference.html |
| Paper PDF | https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Paper-Conference.pdf |
| Supplementary PDF | https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Supplemental-Conference.pdf |
| OpenReview | https://openreview.net/forum?id=KFm2lZiI7n |
| Code | https://github.com/HamsterMimi/MeCo |
| Local PDF | `D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation Supplementary Material.pdf` |
| Local code | `D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation` |

## One-line Summary
> MeCo uses the minimum eigenvalue of layer-wise feature-map correlation matrices as a training-free proxy, enabling one-sample/one-forward NAS ranking and strong zero-shot search results.

## Core Contributions
1. Defines a new zero-cost proxy from [[Minimum Eigenvalue of Correlation]] of feature-map correlations across network layers (main paper, Def. 3 / Eq. 12).
2. Provides a theory link between correlation-based quantity and network trainability kernel behavior (main paper, Theorem 1; supplementary gives full proofs for later theorems).
3. Introduces MeCoopt by adding a weighted maximum-eigenvalue term to improve ranking stability in broader tasks (main paper, Eq. 16 in the reported derivation).
4. Integrates proxy into Zero-Cost-PT style search and reports good correlation/search performance under tiny proxy compute budgets (supplementary, App. C/F).

## Problem Context
### Target problem
- Training-free or zero-shot ranking in [[Neural Architecture Search]] when full training per architecture is too expensive.

### Prior limitation
- Many [[Zero-Cost Proxy]] methods still need more than one batch, backward pass, or have unstable rank correlation across spaces/tasks.

### Why MeCo
- Correlation structure of feature maps is cheap to compute and can be tied to spectral properties that reflect optimization dynamics.

## Method Details
### Proxy definition (MeCo)
For each selected layer feature map `F_l(X)`, build a correlation matrix `P(F_l(X))`, then score by minimum eigenvalue:

$$
S_{MeCo} = \sum_{l=1}^{L} \lambda_{min}(P(F_l(X)))
$$

- Source: main paper Definition 3, Eq. (12).

### MeCoopt extension
Adds weighted maximum-eigenvalue correction:

$$
S_{MeCoopt} = S_{MeCo} + \sum_{l=1}^{L}\xi_l \lambda_{max}(P(F_l(X)))
$$

- Source: main paper derivation around Eq. (16).

### Search algorithm integration
Supplementary Algorithm 1 uses two stages:
1. Architecture proposal by greedy operation/edge selection using MeCo.
2. Architecture validation among candidates with final MeCo ranking.

- Source: supplementary App. C, Algorithm 1.

## Key Experimental Evidence
1. Reported Spearman rank correlation on NATS-Bench-TSS reaches around `0.89/0.88/0.85` (CIFAR-10/CIFAR-100/ImageNet16-120), with one-sample proxy computation.
2. On NAS-Bench-101 (supplementary Table 4), MeCo correlation is reported as `0.44` and outperforms several baselines there.
3. On DARTS-CNN search (supplementary Table 9), MeCo-based Zero-Cost-PT reports competitive test error with low GPU-day search cost.
4. On MobileNet space (supplementary Table 10), MeCo reports `77.8` Top-1 in the shown setup.

## Paper-Code Alignment
1. `correlation/foresight/pruners/measures/meco.py` computes random-input forward features, correlation matrices, eigenvalues, then sums layer minima.
2. NaN/Inf in correlation matrices are zeroed before eigendecomposition in code.
3. `compute_meco` is exposed as a `@measure("meco")` metric, matching search script options.
4. `nasbench201/networks_proposal.py` includes `--proj_crit meco` path for candidate proposal in search.

## Critical View
### Strengths
1. Very low proxy cost; practical for large candidate pools.
2. Clear spectral-statistical interpretation; not purely heuristic.
3. Easy integration into existing zero-cost pipelines.

### Limitations
1. Correlation quality can vary by task/space; not universally dominant.
2. Eigenvalue estimation on tiny samples can be numerically sensitive.
3. Theoretical guarantees are under assumptions; real architectures may only approximately satisfy them.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Minimum Eigenvalue of Correlation]]
