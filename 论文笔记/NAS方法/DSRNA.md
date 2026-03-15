---
title: "DSRNA"
type: method
source_paper: "DSRNA: Differentiable Search of Robust Neural Architectures"
source_note: "[[DSRNA]]"
authors: [Ramtin Hosseini, Xingyi Yang, Pengtao Xie]
year: 2021
venue: CVPR
tags: [nas-method, robust-nas, differentiable-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# DSRNA

## One-line Summary
> DSRNA performs robust differentiable NAS by directly maximizing a differentiable robustness metric (certified-bound or Jacobian-bound) together with validation accuracy.

## Source
- Paper: [DSRNA: Differentiable Search of Robust Neural Architectures](https://arxiv.org/abs/2012.06122)
- HTML: https://arxiv.org/html/2012.06122
- Code: Not found (no official repository link in paper/arXiv page)
- Paper note: [[DSRNA]]

## Applicable Scenarios
- Problem type: Robust neural architecture search for image classification.
- Assumptions: Search space is differentiable and architecture variables can be optimized with gradient-based bilevel optimization.
- Data regime: Supervised CV datasets (CIFAR-10, ImageNet transfer, MNIST).
- Scale / constraints: DSRNA-CB is compute-heavy; DSRNA-Jacobian is lighter.
- Why it fits: Robustness is optimized as an explicit objective instead of indirect regularization only.

## Not a Good Fit When
- You need a very low-cost search budget and cannot afford CB-based bound propagation.
- Your search space is non-differentiable (e.g., purely evolutionary/discrete with no relaxation).
- You require fully reproducible official code from the original authors.

## Inputs, Outputs, and Objective
- Inputs: Differentiable NAS supernet, train/val splits, attack budget parameter(s), tradeoff `gamma`.
- Outputs: Searched robust cell architecture (DSRNA-CB, DSRNA-Jacobian, or DSRNA-Combined).
- Objective: Minimize validation loss while maximizing a robustness metric.
- Core assumptions: Robustness metric `R` is differentiable w.r.t. architecture variables.

## Method Breakdown

### Stage 1: Define Robustness Metric on Architecture Space
- Build differentiable robustness metric `R` from:
  - certified robustness lower bound via linear bound composition; or
  - Jacobian norm bound via first-order approximation.
- Source: Sec. 3.1.1, Sec. 3.1.2, Eq. (1)-(15)

### Stage 2: Robust Bilevel NAS Optimization
- Optimize architecture variables with objective:
  `min_alpha L_val(w*(alpha),alpha) - gamma * R(w*(alpha),alpha)`.
- Inner loop optimizes weights on train set; outer loop optimizes architecture on val set.
- Source: Sec. 3.2, Eq. (16)

### Stage 3: Instantiate Variants
- DSRNA-CB: `R = certified lower bound`.
- DSRNA-Jacobian: `R = Jacobian norm bound`.
- DSRNA-Combined: `R = R_cb + R_jacobian`.
- Source: Sec. 3.2

## Pseudocode
```text
Algorithm: DSRNA
Input: supernet with architecture variables alpha, train data Dtr, val data Dval, tradeoff gamma
Output: robust architecture alpha*

1. Initialize network weights w and architecture variables alpha.
   Source: Sec. 3.2 (DARTS-style setup)
2. For each search step:
   2.1 Update w by descending training loss L(w, alpha, Dtr).
       Source: Eq. (16), inner problem
   2.2 Approximate w*(alpha) with one-step update (DARTS approximation).
       Source: Sec. 3.2 (text after Eq. 16)
   2.3 Compute validation objective:
       J(alpha) = L_val(w*(alpha), alpha) - gamma * R(w*(alpha), alpha).
       Source: Eq. (16)
   2.4 Update alpha by descending J(alpha).
       Source: Eq. (16)
3. Derive final discrete architecture from optimized alpha.
   Source: Inference from DARTS-style differentiable NAS pipeline
```

## Training Pipeline
1. Search phase:
   joint optimization of weights and architecture variables with robust objective.
2. Architecture derivation:
   discretize selected operations from optimized architecture variables.
3. Final training:
   retrain stacked cells from scratch on target dataset.

Sources:
- Sec. 3.2, Sec. 4.2.2

## Inference Pipeline
1. Use searched architecture and trained weights for prediction.
2. Evaluate under clean setting and multiple attacks (PGD/FGSM/C&W/AutoAttack).
3. Optionally verify certified lower bounds with the paper's certification procedure.

Sources:
- Sec. 4.3.1, Sec. 4.3.2, Table 1-6

## Complexity and Efficiency
- Time complexity: Not given in closed-form for the full method.
- Space complexity: Not reported in closed-form.
- Runtime characteristics (single GTX1080Ti):
  - CIFAR-10 search: DSRNA-CB 4 GPU days, DSRNA-Jacobian 0.4 GPU days.
  - MNIST search: DSRNA-CB 1 GPU day, DSRNA-Jacobian 0.2 GPU day.
- Scaling notes: CB variant is more robust but significantly costlier.

## Implementation Notes
- Search space follows PC-DARTS operations (8 candidate ops).
- Small search network: 8 cells, 50 epochs, initial channels 16.
- Final training (CIFAR-10/MNIST): 20 cells, 600 epochs, init channels 36.
- Tradeoff coefficient in paper: `gamma = 0.01`.
- Code status: no official code link found on paper/CVPR/arXiv pages; local implementation not archived.

## Comparison to Related Methods
- Compared with [[SDARTS-ADV]] / [[PC-DARTS-ADV]]:
  DSRNA directly optimizes explicit robustness metric; baselines mainly rely on adversarial perturbation regularization.
- Compared with [[RobNet]]:
  DSRNA keeps much higher clean accuracy while remaining robust.
- Main advantage: explicit robust objective + strong empirical and certified robustness.
- Main tradeoff: CB variant has higher search cost and code unavailability hurts reproducibility.

## Evidence and Traceability
- Key figure(s): Fig. 1 (framework overview in paper)
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5, Table 6
- Key equation(s): Eq. (12)-(16) plus bound construction Eq. (1)-(11)
- Key algorithm(s): optimization procedure described in Sec. 3.2 (detailed algorithm in supplement)

## References
- arXiv: https://arxiv.org/abs/2012.06122
- HTML: https://arxiv.org/html/2012.06122
- Code: Not found
- Local implementation: Not archived
