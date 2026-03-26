---
title: "BioNAS"
type: method
source_paper: "Neural Architecture Search with Mixed Bio-inspired Learning Rules"
source_note: "[[BioNAS]]"
authors: [Imane Hamzaoui, Riyadh Baghdadi]
year: 2025
venue: ECAI 2025 (arXiv preprint)
tags: [nas-method, bio-inspired-learning, adversarial-robustness, darts, evolutionary-search]
created: 2026-03-25
updated: 2026-03-25
---

# BioNAS

## One-line Summary
> BioNAS jointly searches architecture operations and layer-wise bio-inspired learning rules, showing that mixed-rule assignment improves both accuracy and adversarial robustness over single-rule bio-inspired training.

## Source
- Paper: [Neural Architecture Search with Mixed Bio-inspired Learning Rules](https://arxiv.org/abs/2507.13485)
- HTML: https://arxiv.org/html/2507.13485v1
- Code (paper-declared): https://anonymous.4open.science/r/LR-NAS-DFE1
- Paper note: [[BioNAS]]

## Applicable Scenarios
- Problem type: neural architecture search under biological-plausibility constraints.
- Assumptions: different layers may prefer different credit-assignment rules.
- Data regime: supervised image classification (CIFAR / ImageNet-family).
- Scale / constraints: suitable when full BP is not the only acceptable training paradigm and robustness is a priority.
- Why it fits: it turns learning-rule choice into a first-class search variable rather than a fixed global setting.

## Not a Good Fit When
- You need top BP-based NAS accuracy regardless of biological plausibility.
- You require fully reproducible public code right now (anonymous link currently unavailable).
- Your deployment stack cannot support rule-specific backward logic.

## Inputs, Outputs, and Objective
- Inputs: NAS supernet search space, candidate operations, candidate learning rules (FA/uSF/brSF/frSF and optional bio-inspired modules), train/val splits.
- Outputs: discrete architecture with per-edge operation-rule selections and trained model.
- Objective: optimize validation performance and robustness while preserving biologically plausible credit assignment.
- Core assumptions: heterogeneous rule assignment can stabilize optimization and improve search outcomes.

## Method Breakdown

### Stage 1: Build mixed op-rule search space
- Convert each edge candidate from plain operation to operation-rule pair.
- Keep DARTS-like operator families and attach feedback-rule options.
- Source: Sec. 3.2.

### Stage 2: Optimize in BioNAS-DARTS
- Use DARTS bi-level optimization: weights on train, architecture params on validation.
- Use continuous relaxation and one-step approximation to jointly learn parameters.
- Final architecture is obtained by discrete argmax over op-rule logits per edge.
- Source: Sec. 3.3, Eq. (6)-(10), Fig. 2.

### Stage 3: Optimize in BioNAS-EG
- Encode architecture candidates over op-rule choices.
- Use CMA-ES to evolve architecture distribution; use SGD for network weights.
- Source: Sec. 3.3, Eq. (11).

### Stage 4: Robustness evaluation
- Evaluate with white-box and black-box attacks (FGSM/PGD/TPGD/APGD/One-Pixel/Square/Transfer).
- Compare against single-rule and BP-trained baselines.
- Source: Sec. 3.5, Sec. 4.1, Table 4.

## Pseudocode
```text
Algorithm: BioNAS
Input:
  Search graph G with edges E
  Operation set O per edge
  Learning-rule set R per edge
  Training data D_train, validation data D_val
Output:
  Discrete architecture A* with per-edge (op, rule) assignments

1. Construct mixed candidate set C = {(o, r) | o in O, r in R} for each edge.
   Source: Sec. 3.2
2. Initialize supernet weights w and architecture logits alpha.
   Source: Sec. 3.3
3. Repeat search iterations:
   3.1 Update w by minimizing L_train(w, alpha) on D_train.
       Source: Eq. (6), Eq. (8)
   3.2 Update alpha by minimizing L_val(w*, alpha) on D_val.
       Source: Eq. (7), Eq. (9)
4. Discretize architecture by selecting highest-probability (op, rule) per edge.
   Source: Eq. (10), Fig. 2
5. Retrain/evaluate selected architecture and report clean + adversarial metrics.
   Source: Sec. 3.4-3.5, Table 1-4
```

## Training Pipeline
1. Define mixed search space over operation-rule pairs.
2. Run DARTS-style or EG-style search to pick architecture + rule assignment.
3. Retrain selected architecture with reported training protocol.
4. Evaluate clean accuracy and attack robustness.

Sources:
- Sec. 3.2-3.5
- Table 1-4

## Inference Pipeline
1. Use the searched architecture as a fixed network.
2. Run standard forward inference for clean and attacked inputs.
3. Compute task metrics and robustness metrics.

Sources:
- Sec. 4.1
- Table 4

## Complexity and Efficiency
- Search-space growth: approximately `|O| x |R|` per edge compared with operation-only NAS.
- Reported search cost:
  - BioNAS-EG: 0.35 GPU-days.
  - BioNAS-DARTS: 1.37 GPU-days.
- Reported post-search performance:
  - 95.16 (CIFAR-10), 76.48 (CIFAR-100), 43.42 (ImageNet16-120), 60.51 (ImageNet Top-1).

## Implementation Notes
- Rule families used in main results: FA/uSF/brSF/frSF.
- Optional modules explored: Hebbian convolution and predictive-coding convolution (lower accuracy but demonstrates extensibility).
- Robustness tests include both gradient-based and query-based attacks.
- Code archival status:
  - paper-declared anonymous link exists,
  - cloning/checking on 2026-03-25 returns `repository not found`.

## Comparison to Related Methods
- Compared with [[Differentiable Architecture Search]]:
  - DARTS searches operations; BioNAS searches operations plus learning rules.
- Compared with [[Evolutionary Neural Architecture Search]]:
  - BioNAS reuses evolutionary search but enriches genotype with rule-selection dimensions.
- Compared with single-rule bio-inspired training:
  - mixed rules improve both clean accuracy and robustness in reported experiments.
- Main advantage: unified framework for accuracy-robustness tradeoff under biological-plausibility constraints.
- Main tradeoff: larger search space and extra implementation complexity in backward-rule handling.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 3.
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5.
- Key equation(s): Eq. (1)-(5), Eq. (6)-(11).
- Key algorithm(s): DARTS bi-level search instantiation and CMA-ES-based EG instantiation in Sec. 3.3.

## References
- arXiv: https://arxiv.org/abs/2507.13485
- HTML: https://arxiv.org/html/2507.13485v1
- Code: https://anonymous.4open.science/r/LR-NAS-DFE1
- Local implementation: Not archived (anonymous link unavailable on 2026-03-25)

