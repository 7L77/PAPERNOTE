---
title: "RDNAS"
type: method
source_paper: "RDNAS: Robust Dual-Branch Neural Architecture Search"
source_note: "[[RDNAS]]"
authors: [Anonymous Authors]
year: 2025
venue: ICLR 2026 Submission
tags: [nas-method, robust-nas, darts, adversarial-training, shapley]
created: 2026-03-26
updated: 2026-03-26
---

# RDNAS

## One-line Summary

> RDNAS augments DARTS-style robust NAS with a dual-branch cell (normal/robust paths) and a robust Shapley scorer (ROSE: MoM + IQR) to stabilize adversarial search and improve clean-robust trade-off.

## Source

- Paper: [RDNAS: Robust Dual-Branch Neural Architecture Search](https://openreview.net/pdf?id=JWW1hhEJTF)
- HTML: https://openreview.net/forum?id=JWW1hhEJTF
- Code: No explicit official repository URL in paper PDF; OpenReview supplementary link returns HTTP 403 in current environment.
- Paper note: [[RDNAS]]

## Applicable Scenarios

- Problem type: adversarially robust cell-based NAS for image classification.
- Assumptions: robust ranking can be recovered from noisy adversarial marginal gains via robust statistics.
- Data regime: supervised classification with white-box attack training/evaluation.
- Scale / constraints: useful when full robust retraining for each candidate is too expensive.
- Why it fits: combines small-sample search with robustness-aware operation scoring.

## Not a Good Fit When

- You need transformer/hybrid search spaces beyond DARTS-like cells.
- You need fully decoupled architecture evaluation independent of adversarial training recipe.
- You require officially packaged code for immediate reproduction.

## Inputs, Outputs, and Objective

- Inputs: DARTS-style supernet edges/ops, branch-specific logits, train/validation splits, PGD attack settings.
- Outputs: discretized robust architecture with normal/reduce/robust cell parameters.
- Objective: jointly improve clean accuracy and adversarial robustness under constrained search budget.
- Core assumptions:
  - branch decoupling reduces objective interference,
  - ROSE improves operation ranking stability under noisy gradients.

## Method Breakdown

### Stage 1: Dual-branch representation design

- Replace normal cell with dual-branch cell: normal path + robust path.
- Fuse by ECA to avoid static equal weighting.
- Source: Sec. 3.2, Eq. (6)-(11), Fig. 2.

### Stage 2: Adversarial bilevel search

- Inner loop trains weights with PGD-generated adversarial samples.
- Outer loop updates architecture logits with ROSE-weighted validation objective.
- Source: Sec. 3.3, Eq. (12)-(14), Algorithm 1.

### Stage 3: ROSE robust operation scoring

- Compute clean/adversarial marginal gains per op.
- Standardize gains, compute IQR outlier score \(v\), MoM score \(m\), then combine:
  \[
  \mathrm{Score}=(1-\beta)m+\beta v
  \]
- Source: Sec. 3.4, Eq. (15)-(19).

## Pseudocode

```text
Algorithm: RDNAS Search
Input: search space S, warm-up Nw, search epochs Ns, Shapley samples S_num,
       MoM groups G, IQR sensitivity gamma, train set D_train, val set D_val
Output: searched architecture A*

1. Initialize branch-specific architecture logits alpha and network weights omega.
   Source: Alg. 1 (line 3)
2. For epoch = 1..(Nw + Ns):
   2.1 Update omega on D_train with adversarial training loss.
       Source: Sec. 3.3, Eq. (12), Alg. 1 (line 5)
   2.2 If epoch > Nw:
       - Estimate clean/adv marginal deltas per op.
         Source: Sec. 3.4, Eq. (15)
       - Compute ROSE score using standardized gains + IQR + MoM.
         Source: Sec. 3.4, Eq. (16)-(19)
       - Update alpha by ROSE score and row-normalize.
         Source: Alg. 1 (line 8-10)
3. Discretize by selecting max-logit op on each edge to form A*.
   Source: Sec. 3.3, Eq. (14), Alg. 1 (line 13)
```

## Training Pipeline

1. Search model: 10 cells, initial channels 32.
2. Search attack: PGD-7, \( \epsilon=8/255 \), step \(2/255\).
3. Small-sample search: CIFAR-10 uses 1000 train / 500 val samples.
4. Retrain selected architecture 120 epochs with adversarial training.
5. Evaluate under FGSM, PGD20/100, APGD-CE, AutoAttack.

Sources:

- Sec. 4.2, Table 1.

## Inference Pipeline

1. Use discretized architecture after robust retraining.
2. Report clean + attack accuracies on target dataset.
3. Optionally transfer searched topology across datasets without re-search.

Sources:

- Sec. 4.3-4.5, Table 2-3.

## Complexity and Efficiency

- Time complexity: not explicitly given in closed form.
- Space complexity: not explicitly given.
- Runtime characteristics: search budget reported as 0.2 GPU-days.
- Scaling notes: dual-branch increases FLOPs (1.30G on CIFAR-10 setting) but improves robustness metrics.

## Implementation Notes

- Branch logits are maintained independently for normal/reduce/robust cell types.
- ECA is lightweight and empirically better than CBAM/ECAM in their appendix.
- ROSE is enabled by default in search; disabling it increases run-to-run variability.
- Local code archive status:
  - `D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search/README.md` records supplementary link and 403 issue.

## Comparison to Related Methods

- Compared with [[RACL]] / [[AdvRush]]:
  - better white-box robustness in most columns, but AA slightly below best baseline.
- Compared with [[LRNAS]]:
  - both robust NAS, but RDNAS emphasizes dual-branch topology + robust Shapley scoring.
- Main advantage: robust search stability under noisy adversarial gradients.
- Main tradeoff: evaluation remains tightly coupled with adversarial training setup.

## Evidence and Traceability

- Key figure(s): Fig. 2 (overall framework), Fig. 4 (searched cells).
- Key table(s): Table 1, Table 4, Table 5, Table 10.
- Key equation(s): Eq. (6)-(14), Eq. (15)-(19).
- Key algorithm(s): Algorithm 1.

## References

- OpenReview PDF: https://openreview.net/pdf?id=JWW1hhEJTF
- OpenReview forum: https://openreview.net/forum?id=JWW1hhEJTF
- Code (supplementary): https://openreview.net/attachment?id=JWW1hhEJTF&name=supplementary_material
- Local implementation: D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search
