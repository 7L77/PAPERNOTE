---
title: "NADAR"
type: method
source_paper: "Neural Architecture Dilation for Adversarial Robustness"
source_note: "[[NADAR]]"
authors: [Yanxi Li, Zhaohui Yang, Yunhe Wang, Chang Xu]
year: 2021
venue: NeurIPS
tags: [nas-method, robust-nas, adversarial-robustness, architecture-dilation]
created: 2026-03-15
updated: 2026-03-15
---

# NADAR

## One-line Summary
> NADAR boosts adversarial robustness by attaching searched dilation cells to a fixed strong backbone, while constraining standard loss and FLOPs during robust search.

## Source
- Paper: [Neural Architecture Dilation for Adversarial Robustness](https://openreview.net/forum?id=55FrYwhCN6)
- HTML: https://openreview.net/forum?id=55FrYwhCN6
- Code: https://github.com/liyanxi12/NADAR (unavailable as of 2026-03-15)
- Paper note: [[NADAR]]

## Applicable Scenarios
- Problem type: robust image classification architecture optimization.
- Assumptions: a backbone with satisfactory clean accuracy is available.
- Data regime: labeled image data with adversarial training loop.
- Scale / constraints: suitable when full robust NAS from scratch is too costly.
- Why it fits: architecture search is focused on an additive branch, not the full model, and can include FLOPs budget.

## Not a Good Fit When
- You do not have a reliable pretrained backbone.
- You need strict certified robustness guarantees (not empirical attack robustness).
- The target architecture cannot be decomposed into backbone blocks with additive feature fusion.

## Inputs, Outputs, and Objective
- Inputs: backbone network `f_b`, search space for dilation cells, adversarial training setup (`epsilon`, attack steps), FLOPs budget preference.
- Outputs: hybrid architecture `f_hyb = f_b + f_d` and trained robust model.
- Objective: minimize adversarial validation loss under standard-loss and FLOPs constraints.
- Core assumptions: dilation branch can capture robust features complementary to backbone features.

## Method Breakdown

### Stage 1: Build Hybrid Network by Dilation
- Split backbone into `L` blocks and attach one NAS cell per block.
- Fuse each block output by element-wise sum.
- Source: Sec. 3.1, Fig. 1, Eq. (2)

### Stage 2: Differentiable Dilation Search with FLOPs Modeling
- Use NASNet-like cell search space and differentiable edge/operation mixing.
- Use partial channel connections to reduce search memory/compute.
- Estimate expected FLOPs under architecture probabilities.
- Source: Sec. 3.1, Sec. 3.3, Eq. (8), Eq. (9), Eq. (10), Eq. (11)

### Stage 3: Constrained Bi-level Optimization via ADMM
- Upper level: optimize architecture parameters for adversarial validation objective.
- Lower level: optimize dilation weights for adversarial training objective.
- Enforce standard-loss constraints at both levels.
- Source: Sec. 3.4, Eq. (12)-(22)

### Stage 4: Discretize and Retrain
- Derive final discrete architecture from searched supernet.
- Retrain/evaluate under selected adversarial training settings (PGD/FAT/TRADES).
- Source: Sec. 5.2, Sec. 5.5, Table 1, Table 6

## Pseudocode
```text
Algorithm: NADAR
Input: pretrained backbone f_b, dilation search space S_d, train/val data, attack config A
Output: robust hybrid network f_hyb*

1. Partition f_b into L resolution-aligned blocks.
   Source: Sec. 3.1
2. Attach one searchable dilation cell per block; fuse by z^(l)=f_b^(l)+f_d^(l).
   Source: Fig. 1, Eq. (2)
3. Define adversarial objectives for train/val and standard-loss constraints.
   Source: Eq. (3), Eq. (4), Eq. (7), Eq. (13), Eq. (14)
4. Add FLOPs-aware term using expected FLOPs under architecture probabilities.
   Source: Eq. (10), Eq. (11), Eq. (12)
5. Run alternating ADMM updates:
   5.1 update architecture params alpha_d and lambda_1 (upper level),
   5.2 update weights omega_d and lambda_2 (lower level).
   Source: Eq. (15)-(22)
6. Discretize architecture and retrain final hybrid model with adversarial training.
   Source: Sec. 5.2, Inference from source
```

## Training Pipeline
1. Train or load a strong clean backbone.
2. Search dilation architecture with adversarial objective + standard constraint + FLOPs term.
3. Export discrete architecture.
4. Retrain/evaluate with PGD-7 (and optionally FAT/TRADES variants).

Sources:
- Sec. 3.1-3.4
- Sec. 5.1, Sec. 5.2, Sec. 5.5

## Inference Pipeline
1. Run forward pass through backbone and dilation branch in parallel per block.
2. Sum block-level features and produce final logits.
3. Use standard classifier head.

Sources:
- Eq. (2)
- Inference from source

## Complexity and Efficiency
- Added parameters/FLOPs depend on dilation branch size.
- FLOPs-aware objective reduces dilation overhead:
  NADAR-B has lower added params/FLOPs than NADAR-A with small robustness drop.
- Search remains costly due adversarial training but less than robust NAS-from-scratch.

## Implementation Notes
- Search space: NASNet-like cell topology.
- Optimization: differentiable supernet + ADMM constraints.
- Cost control: partial channel connections + FreeAT during search.
- Practical gotcha: removing standard constraint hurts trade-off sharply (Table 7).
- Code status: official URL listed on OpenReview but currently unavailable, so code was not archived locally.

## Comparison to Related Methods
- Compared with [[RACL]]: NADAR optimizes an additive dilation branch and explicitly constrains standard loss.
- Compared with [[RobNet]]: NADAR does not require searching full architecture from scratch.
- Main advantage: better robustness gains at smaller natural-accuracy drop in reported settings.
- Main tradeoff: extra search/training cost and dependence on a strong initial backbone.

## Evidence and Traceability
- Key figure(s): Fig. 1
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 6, Table 7
- Key equation(s): Eq. (1), Eq. (2), Eq. (7), Eq. (10), Eq. (12), Eq. (15)-(22)
- Key algorithm(s): ADMM-style alternating constrained updates in Sec. 3.4

## References
- OpenReview: https://openreview.net/forum?id=55FrYwhCN6
- Code: https://github.com/liyanxi12/NADAR (unavailable as of 2026-03-15)
- Local implementation: Not archived
