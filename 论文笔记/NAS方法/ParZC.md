---
title: "ParZC"
type: method
source_paper: "ParZC: Parametric Zero-Cost Proxies for Efficient NAS"
source_note: "[[ParZC]]"
authors: [Peijie Dong, Lujun Li, Zhenheng Tang, Xiang Liu, Zimian Wei, Qiang Wang, Xiaowen Chu]
year: 2025
venue: AAAI
tags: [nas-method, nas, zero-cost-proxy, predictor-based]
created: 2026-03-17
updated: 2026-03-17
---

# ParZC

## One-line Summary
> ParZC turns node-wise zero-cost statistics into a trainable architecture ranking predictor, and optimizes rank consistency directly with DiffKendall.

## Source
- Paper: [ParZC: Parametric Zero-Cost Proxies for Efficient NAS](https://arxiv.org/abs/2402.02105)
- HTML: https://arxiv.org/html/2402.02105
- Code: Not found on paper/arXiv page at time of note creation
- Paper note: [[ParZC]]

## Applicable Scenarios
- Problem type: Low-cost architecture ranking for NAS candidate filtering.
- Assumptions: Node-wise ZC signals are informative but heterogeneous in contribution.
- Data regime: Small amount of architecture-accuracy labels (e.g., 0.02%-10% splits).
- Scale / constraints: Need better ranking than plain ZC sum under tight compute budget.
- Why it fits: Combines training-free node features with lightweight rank-supervised predictor.

## Not a Good Fit When
- No label budget at all (cannot train MABN branch).
- Search space statistics differ drastically from training split and domain shift is severe.
- You need strict reproducibility from official code (repo not explicitly released).

## Inputs, Outputs, and Objective
- Inputs: Node-wise ZC statistics (from weight/activation/gradient/Hessian proxies), plus architecture encoding when used with NP setup.
- Outputs: Scalar ranking score per architecture.
- Objective: Maximize rank correlation between predicted ranking and ground-truth ranking.
- Core assumptions: Node importance is non-uniform and uncertainty-aware aggregation improves ranking.

## Method Breakdown
### Stage 1: Node-wise ZC extraction and normalization
- Extract per-node proxy values for each architecture and apply min-max scaling.
- Source: Sec. 3.1, Fig. 5.

### Stage 2: MABN uncertainty-aware mixing
- Feed normalized node-wise vectors into Bayesian layers + mixer blocks for inter-segment interaction.
- Source: Sec. 3.2, Fig. 5.

### Stage 3: Differentiable rank optimization
- Train with DiffKendall to optimize ranking consistency directly.
- Source: Sec. 3.3.

### Stage 4: Training-free variant ParZC†
- Apply non-negative sinusoidal node weighting to existing ZC proxies.
- Source: Sec. 3.4, Eq. (1).

## Pseudocode
```text
Algorithm: ParZC ranking predictor
Input: Architecture set A, node-wise proxy extractor Z, train split D={(a_i, y_i)}
Output: Ranking score function f_theta(a)

1. For each architecture a in A:
   compute node-wise proxy vector v_a = Normalize(Z(a)).
   Source: Sec. 3.1, Fig. 5
2. Train MABN predictor f_theta on D:
   s_i = f_theta(v_{a_i})
   optimize DiffKendall(s, y).
   Source: Sec. 3.2-3.3
3. Rank architectures by s = f_theta(v_a) in descending order.
   Source: Sec. 4 (ranking evaluation protocol)
4. (Optional) Replace trained branch with ParZC† node weighting for training-free scoring.
   Source: Sec. 3.4
```

## Training Pipeline
1. Sample a small labeled architecture subset from search space.
2. Build node-wise ZC vectors and normalize each architecture sample.
3. Train MABN with Adam + DiffKendall (or ablation losses).
4. Evaluate SP/KD correlation on held-out architectures.

Sources:
- Sec. 4 (Datasets and Implementation Details), Tab. 2/3/8.

## Inference Pipeline
1. Compute node-wise ZC vectors for candidate architectures.
2. Forward through trained ParZC predictor to get ranking scores.
3. Select top-ranked architectures for full training/evaluation.

Sources:
- Sec. 4 (comparison and search results), Tab. 4.

## Complexity and Efficiency
- Time complexity: Dominated by node-wise proxy extraction + MABN forward/backward on sampled architectures.
- Space complexity: Stores node-wise proxy tensors and predictor parameters.
- Runtime characteristics: Reported training cost around 3000 GPU sec (~50 GPU minutes) on NB201 setup.
- Scaling notes: Better sample efficiency than many predictors at low sample budgets (e.g., 78-sample NB201 split).

## Implementation Notes
- Optimizer and schedule: Adam, lr=1e-4, wd=1e-3, train/eval batch size 10/50.
- Training epochs: NB101 150, NB201 200, NDS 296.
- DiffKendall smoothing coefficient: alpha=0.5.
- Optional NP-style architecture encoding can be combined for stronger predictor performance.
- Official code link is not explicitly provided in paper/arXiv page, so implementation details are paper-derived.

## Comparison to Related Methods
- Compared with [[EZNAS]]: ParZC improves ranking while requiring far fewer samples in low-sample settings.
- Compared with [[HNAS]]: ParZC reaches stronger KD under same sample budgets in reported comparisons.
- Main advantage: Better ranking quality and sample efficiency by modeling node heterogeneity + uncertainty.
- Main tradeoff: Needs small supervised subset (not purely training-free unless using ParZC†).

## Evidence and Traceability
- Key figure(s): Fig. 2 (node heterogeneity), Fig. 4 (sample efficiency), Fig. 5 (framework), Fig. 6 (rank visualization).
- Key table(s): Tab. 1 (cross-benchmark SP/KD), Tab. 2/3 (predictor comparisons), Tab. 4 (search performance), Tab. 8 (loss ablation).
- Key equation(s): Node-wise scaling (Sec. 3.1), Bayesian reparameterization (Sec. 3.2), DiffKendall (Sec. 3.3), non-negative weighting Eq. (1).
- Key algorithm(s): No explicit algorithm box in main text; pipeline reconstructed from Sec. 3-4.

## References
- arXiv: https://arxiv.org/abs/2402.02105
- HTML: https://arxiv.org/html/2402.02105
- Code: Not found on paper/arXiv page at time of note creation
- Local implementation: Not archived
