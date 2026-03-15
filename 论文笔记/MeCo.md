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
local_pdf: D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation.pdf
local_pdf_supplementary: D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation Supplementary Material.pdf
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
| Local PDF (main) | `D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation.pdf` |
| Local PDF (supp) | `D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation Supplementary Material.pdf` |
| Local code | `D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation` |

## One-line Summary
> MeCo uses the minimum eigenvalue of layer-wise feature-map Pearson correlation matrices as a training-free proxy, requiring only one random sample and one forward pass.

## Core Contributions
1. Proposes MeCo based on [[Minimum Eigenvalue of Correlation]] over intermediate feature maps (Def. 3, Eq. 12).
2. Gives theory linking Pearson-correlation spectral quantity to convergence/generalization in over-parameterized settings (Theorem 2/3, proofs in supplementary).
3. Proposes MeCoopt to reduce channel-sensitivity by fixed channel sampling and weighted aggregation (Eq. 13).
4. Shows strong ranking/search performance on NATS-Bench, NAS-Bench-301, and DARTS-style search integration.

## Problem Context
### Target problem
- Training-free or zero-shot ranking in [[Neural Architecture Search]] when full training per architecture is too expensive.

### Prior limitation
- Many [[Zero-Cost Proxy]] methods still need more than one batch, backward pass, or have unstable rank correlation across spaces/tasks.

### Why MeCo
- Correlation structure of feature maps is cheap to compute and can be tied to spectral properties that reflect optimization dynamics.

## Method Details
### Proxy definition (MeCo)
For each layer feature map `f^i(X; θ)`, construct Pearson correlation matrix and sum layer-wise minimum eigenvalues:

$$
MeCo := \sum_{i=1}^{D} \lambda_{min}(P(f^i(X; \theta)))
$$

- Source: main paper Def. 3, Eq. (12).

### MeCoopt extension
Main-text MeCoopt (Section 5.1) is:

$$
MeCoopt := \sum_{i=1}^{D} \frac{c(i)}{n}\cdot \lambda_{min}(P^{\cap}_i)
$$

- where `c(i)` is channel count of layer `i`, `n` is fixed sampled channel number, and `P^{\cap}_i` is correlation matrix from sampled channels.
- Source: main paper Eq. (13), Sec. 5.1.

### Search algorithm integration
Supplementary Algorithm 1 uses two stages:
1. Architecture proposal by greedy operation/edge selection using MeCo.
2. Architecture validation among candidates with final MeCo ranking.

- Source: supplementary App. C, Algorithm 1.

## Key Experimental Evidence
1. NATS-Bench-TSS (main Table 1): `0.894±0.003 / 0.883±0.005 / 0.845±0.004` on CIFAR-10/100/ImageNet16-120.
2. NATS-Bench-SSS (main Table 1): strong negative correlation appears for MeCo (`-0.79/-0.87/-0.86`), motivating MeCoopt.
3. NAS-Bench-301 (main Table 2): MeCo/MeCoopt are top (`0.70±0.01 / 0.71±0.01`).
4. DARTS-CNN CIFAR-10 search (main Table 4): MeCo-based Zero-Cost-PT reports `2.69±0.05` test error with `0.08` GPU days.
5. Data dependence test (main Table 3): with random data, MeCo remains high-correlation compared with NTK baseline.

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
1. Channel-count variation can flip correlation sign in some spaces (explicitly discussed in Sec. 4.2/5.1).
2. Eigenvalue estimation can be numerically unstable with tiny sampled channels.
3. Theoretical guarantees rely on over-parameterized assumptions and approximations from CNN to FC form.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Minimum Eigenvalue of Correlation]]
