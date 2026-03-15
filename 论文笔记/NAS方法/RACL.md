---
title: "RACL"
type: method
source_paper: "Adversarially Robust Neural Architectures"
source_note: "[[RACL]]"
authors: [Minjing Dong, Yanxi Li, Yunhe Wang, Chang Xu]
year: 2025
venue: TPAMI
tags: [nas-method, robust-nas, differentiable-nas, lipschitz]
created: 2026-03-15
updated: 2026-03-15
---

# RACL

## One-line Summary

> RACL turns architecture parameters in differentiable NAS into log-normal random variables and enforces a probabilistic Lipschitz upper-bound constraint, so robust architectures are searched with explicit confidence rather than plain argmax.

## Source

- Paper: [Adversarially Robust Neural Architectures](https://doi.org/10.1109/TPAMI.2025.3542350)
- HTML: Not provided in paper
- Code: Not found in paper (no official repository link in the TPAMI version)
- Paper note: [[RACL]]

## Applicable Scenarios

- Problem type: adversarially robust neural architecture search for image classification.
- Assumptions: smaller network Lipschitz upper bound correlates with better adversarial robustness.
- Data regime: supervised image classification with train/val split for bi-level NAS updates.
- Scale / constraints: DARTS-like cell search spaces where mixed operations and edge weights are available.
- Why it fits: it directly ties architecture sampling to robustness-relevant constraints through probability control.

## Not a Good Fit When

- You need a method with official code and plug-and-play training scripts.
- Your search space is non-cell-based or not differentiable.
- You prioritize ultra-low search cost over robust performance gains.

## Inputs, Outputs, and Objective

- Inputs: search space operations, split datasets (`D_T`, `D_V`), perturbation settings, confidence hyperparameter `eta`.
- Outputs: searched normal/reduction cells and retrained robust model.
- Objective: minimize classification loss plus gradient-norm term under confidence-aware Lipschitz bound constraints.
- Core assumptions: log-normal approximation of edge/node/network Lipschitz terms is adequate for optimization.

## Method Breakdown

### Stage 1: Robustness Formulation via Lipschitz Bounds

- Start from adversarial objective and bound loss change by network Lipschitz constant.
- Convert robust architecture search into constrained optimization on `lambda_F` bounds.
- Source: Sec. III-A, Eq. (1)-(4).

### Stage 2: Decompose Network Lipschitz by NAS Structure

- Use DARTS-style mixed operation with architecture parameters `alpha` and `beta`.
- Derive network-level upper bound as product of node/cell terms determined by architecture choices.
- Source: Sec. III-B, Eq. (5), Eq. (7)-(10).

### Stage 3: Confidence-aware Architecture Sampling

- Sample `alpha` and `beta` from multivariate log-normal distributions.
- Propagate distributions to edge/node/network Lipschitz upper bounds using log-normal properties.
- Source: Sec. III-C, Eq. (11)-(12), Fig. 1-2.

### Stage 4: Probabilistic Constraint + ADMM Optimization

- Enforce `Pr(lambda_F <= lambda_bar_F) >= eta`.
- Rewrite via CDF to get tractable constraint; optimize with ADMM-style primal-dual updates.
- Source: Sec. III-C, Eq. (13)-(19), Algorithm 1.

## Pseudocode

```text
Algorithm: RACL
Input: Search space O, train split D_T, val split D_V, confidence eta, ADMM penalty rho
Output: Robust architecture A* (normal + reduction cells)

1. Initialize log-normal distributions for architecture parameters:
   alpha ~ LN(mu_alpha, Sigma_alpha), beta ~ LN(mu_beta, Sigma_beta).
   Source: Sec. III-C, Algorithm 1

2. Sample alpha, beta with reparameterization and optimize supernet weights W on D_T:
   minimize L_CE + ||grad_x F||.
   Source: Algorithm 1, Eq. (16)

3. Optimize distribution parameters (mu_alpha, Sigma_alpha, mu_beta, Sigma_beta) on D_V
   under confidence-aware Lipschitz constraint using ADMM updates.
   Source: Algorithm 1, Eq. (17)-(19)

4. Repeat steps 2-3 until convergence, then sample discrete normal/reduction cells
   according to learned architecture distributions.
   Source: Algorithm 1, Sec. III-C

5. Retrain sampled architecture from scratch with adversarial training and evaluate
   under FGSM/MIM/PGD/CW/AutoAttack.
   Source: Sec. IV-A/B
```

## Training Pipeline

1. Search phase on CIFAR-10 with split train/val optimization.
2. Supernet training for 50 epochs (batch 128, SGD for weights, Adam for architecture distribution parameters).
3. Sample searched architecture from learned distributions.
4. Retrain 20-cell architecture from scratch with FAT adversarial training for fair comparison.

Sources:

- Sec. IV-A
- Algorithm 1

## Inference Pipeline

1. Use retrained searched model for clean and adversarial evaluation.
2. Evaluate white-box robustness with FGSM, MIM, PGD, CW, AutoAttack.
3. Evaluate transfer-based black-box robustness by source-target cross attacks.

Sources:

- Sec. IV-B/D/E
- Table I-VIII

## Complexity and Efficiency

- Time complexity: not reported in closed form.
- Space complexity: not reported in closed form.
- Runtime characteristics: reported search cost around `0.5 GPU-day`.
- Scaling notes: still requires full retraining and adversarial evaluation after search.

## Implementation Notes

- Search space ops: sep conv (3x3/5x5), dilated sep conv (3x3/5x5), max/avg pooling, skip, zero.
- Supernet: 8 cells (6 normal + 2 reduction), each with 6 nodes.
- Search optimization: SGD (`lr=0.1`, momentum `0.9`, weight decay `3e-4`) for weights; Adam (`lr=6e-4`, weight decay `1e-3`) for architecture distribution params.
- Retrain with AT: 100 epochs, SGD (`lr=0.1`, momentum `0.9`, weight decay `2e-4`), gradient clipping `5`.
- Confidence hyperparameter: best `eta=0.9` from ablation.

## Comparison to Related Methods

- Compared with [[DARTS]] / [[PC-DARTS]]: adds robustness-oriented probabilistic constraints instead of plain architecture logits.
- Compared with RobNet/ABanditNAS/AdvRush/DSRNA: keeps differentiable-search efficiency while improving robustness on most reported attacks.
- Main advantage: explicit confidence-aware robust architecture sampling.
- Main tradeoff: approximation assumptions (log-normal sum) and no official code release.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5.
- Key table(s): Table I-X.
- Key equation(s): Eq. (2)-(4), Eq. (5), Eq. (7)-(12), Eq. (13)-(16), Eq. (17)-(19).
- Key algorithm(s): Algorithm 1.

## References

- DOI: https://doi.org/10.1109/TPAMI.2025.3542350
- HTML: Not provided in paper
- Code: Not found in paper
- Local implementation: Not archived
