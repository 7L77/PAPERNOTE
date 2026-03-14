---
title: "MeCo"
type: method
source_paper: "MeCo: Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation"
source_note: "[[MeCo]]"
authors: [Tangyu Jiang, Haodi Wang, Rongfang Bie]
year: 2023
venue: NeurIPS
tags: [nas-method, nas, training-free, zero-cost-proxy]
created: 2026-03-14
updated: 2026-03-14
---

# MeCo

## One-line Summary
> MeCo ranks architectures by summing layer-wise minimum eigenvalues of feature-map correlation matrices from one random input forward pass, then plugs this score into zero-shot NAS search.

## Source
- Paper: [MeCo: Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation](https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Paper-Conference.pdf)
- Supplementary: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Supplemental-Conference.pdf
- OpenReview: https://openreview.net/forum?id=KFm2lZiI7n
- Code: https://github.com/HamsterMimi/MeCo
- Paper note: [[MeCo]]

## Applicable Scenarios
- Problem type: Training-free architecture ranking and zero-shot candidate screening in NAS.
- Assumptions: Feature-map correlations from random-input forward pass contain useful ranking signal.
- Data regime: One random sample can be used for proxy scoring.
- Scale/constraints: Large candidate sets, strict compute budget.
- Why it fits: Avoids heavy training/backprop loops for every candidate architecture.

## Not a Good Fit When
- Rank quality is highly unstable under very small-sample correlation estimates.
- Architecture internals do not expose stable feature maps per layer.
- Task/domain shift breaks correlation-performance relationship.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture `A`, random input `X`, selected layer features `F_l(X)`.
- Outputs: Scalar proxy score `S_MeCo` (or `S_MeCoopt`) for ranking.
- Objective: Improve rank correlation between proxy score and final trained accuracy.
- Core assumptions: Spectral behavior of feature-map correlation captures trainability-related structure.

## Method Breakdown
### Stage 1: Extract feature-map correlations
- Run one forward pass with random input.
- For each chosen layer, flatten feature map and build correlation matrix.
- Source: main paper Def. 3 / Eq. (12); code `correlation/foresight/pruners/measures/meco.py`.

### Stage 2: Compute spectral proxy
- Get minimum eigenvalue per layer correlation matrix.
- Sum over layers to obtain `S_MeCo`.
- Source: main paper Eq. (12).

### Stage 3: Optional MeCoopt correction
- Add weighted maximum-eigenvalue term:
  `S_MeCoopt = S_MeCo + sum_l xi_l * lambda_max(P(F_l(X)))`.
- Source: main paper derivation around Eq. (16).

### Stage 4: NAS integration
- Use MeCo in architecture proposal and candidate validation loop.
- Source: supplementary App. C Algorithm 1.

## Pseudocode
```text
Algorithm: MeCo-based zero-shot NAS
Input: Supernet A0, candidate operations O, edges E, nodes N, number of candidates K
Output: Best architecture Abest

1. For each candidate architecture Ai to be built:
   1.1 Repeatedly choose operations/edges using MeCo score on partially specified architecture.
       Source: Supplementary App. C Algorithm 1 (Stage 1)
   1.2 Keep top edges per node under the MeCo criterion to form Ai.
       Source: Supplementary App. C Algorithm 1
2. Evaluate each Ai with final MeCo score and choose best:
   Abest = argmax_i MeCo(Ai)
   Source: Supplementary App. C Algorithm 1 (Stage 2)
3. (Optional) Use MeCoopt instead of MeCo.
   Source: Main paper Eq. (16), Inference from source
```

## Training Pipeline
1. Build/search candidate architectures via MeCo-based zero-shot loop.
2. Select top architecture under proxy ranking.
3. Fully train selected architecture with standard benchmark protocol.
4. Report final test metrics and compare against other proxies.

Sources:
- Supplementary App. C/F, related result tables.

## Inference Pipeline
1. Use selected/trained architecture for normal forward inference.
2. MeCo itself is only for search-time ranking, not test-time deployment.

Sources:
- Inference from source.

## Complexity and Efficiency
- Time complexity: Dominated by per-layer correlation + eigendecomposition (`lambda_min`), plus search loop over candidates.
- Space complexity: Stores feature tensors/correlation matrices for selected layers.
- Runtime characteristics: One random-sample forward pass per proxy evaluation in reported setup.
- Scaling notes: Candidate count and number of scored layers directly affect total search overhead.

## Implementation Notes
- Random input creation appears in code (`torch.randn(size=(1,3,64,64))`).
- Forward hooks are registered to collect layer outputs.
- Correlation matrix uses `torch.corrcoef`; NaN/Inf are clamped to zero before eigen solve.
- Eigenvalues come from `torch.linalg.eig`; per-layer minimum eigenvalue is accumulated.
- Search script allows `--proj_crit meco` in NAS-Bench-201 flow.
- Paper and code are consistent on "single random sample + single forward pass" design intent.

## Comparison to Related Methods
- Compared with SNIP/Grasp/SynFlow/Jacov: MeCo emphasizes correlation-spectrum signal and very low sample cost.
- Main advantage: Strong search/rank behavior with minimal proxy compute.
- Main tradeoff: Sensitivity to numerical/statistical quality of correlation estimates.

## Evidence and Traceability
- Key paper definition: Def. 3 / Eq. (12) (main paper).
- Key extension: Eq. (16) (main paper).
- Key algorithm: App. C Algorithm 1 (supplementary).
- Key empirical tables: Supplementary Tables 3/4/9/10 (as reported in the supplementary PDF).
- Key code paths:
  - `correlation/foresight/pruners/measures/meco.py`
  - `nasbench201/networks_proposal.py`
  - `README.md`

## References
- NeurIPS abstract page: https://proceedings.neurips.cc/paper_files/paper/2023/hash/95a50c26d63cf9f3dcf67784f40eb6fd-Abstract-Conference.html
- Paper PDF: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Paper-Conference.pdf
- Supplementary PDF: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Supplemental-Conference.pdf
- OpenReview: https://openreview.net/forum?id=KFm2lZiI7n
- Code: https://github.com/HamsterMimi/MeCo
- Local implementation: D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation
