---
title: "NARes"
type: method
source_paper: "A Neural Architecture Dataset for Adversarial Robustness"
source_note: "[[NARes]]"
authors: [Bowen Zheng, Ran Cheng, Shihua Huang, Zhichao Lu, Vishnu Boddeti]
year: 2025
venue: ICLR 2025 (OpenReview submission)
tags: [nas-method, robustness-dataset, adversarial-robustness, macro-search-space, wrn]
created: 2026-03-23
updated: 2026-03-23
---

# NARes

## One-line Summary
> NARes exhaustively adversarially trains and evaluates a WRN macro search space, turning expensive robust-NAS exploration into a queryable benchmark with rich robustness diagnostics.

## Source
- Paper: [A Neural Architecture Dataset for Adversarial Robustness](https://openreview.net/forum?id=AZVvTBxTdZ)
- PDF: https://openreview.net/pdf/adb9acc706c4b858a6448cb218e58621b71dd419.pdf
- Supplementary: https://openreview.net/attachment?id=AZVvTBxTdZ&name=supplementary_material
- Code: Not publicly linked in the current OpenReview/PDF version (checked 2026-03-23)
- Paper note: [[NARes]]

## Applicable Scenarios
- Problem type: Robust NAS benchmarking and architecture-principle validation.
- Assumptions: Offline tabular robustness data is acceptable; target study concerns WRN-style macro design.
- Data regime: CIFAR-10 adversarial training and evaluation.
- Scale / constraints: Useful when repeated full adversarial training is too expensive.
- Why it fits: NARes decouples expensive robustness measurement from downstream NAS/proxy iterations.

## Not a Good Fit When
- You need online training inside a new search space.
- You require non-WRN architecture families as the primary target.
- You need large-scale non-CIFAR validation without additional retraining.

## Inputs, Outputs, and Objective
- Inputs: Search space vector `[D1, W1, D2, W2, D3, W3]`, CIFAR-10 data, AT hyperparameters, attack suite.
- Outputs: Per-epoch logs, per-architecture checkpoints and robustness metrics (clean, FGSM, PGD20, PGD-CW40, AA-Compact, corruption metrics, stable accuracy, empirical Lipschitz).
- Objective: Build a high-resolution architecture-performance landscape for adversarial robustness and NAS.
- Core assumptions: A dense, consistently trained macro-space dataset can reveal robust architecture patterns and support reproducible NAS comparisons.

## Method Breakdown

### Stage 1: Define WRN macro search space
- Use pre-activation WRN blocks with 3 stages.
- Encode architecture as `[D1, W1, D2, W2, D3, W3]`, with 5 choices per dimension.
- Total architecture count: `5^6 = 15,625`.
- Source: Sec. 3.1, Fig. 1.

### Stage 2: Train all architectures with unified adversarial protocol
- Standard PGD adversarial training for 100 epochs on CIFAR-10.
- LR decays at epoch 75 and 90.
- Early stopping by validation PGD-CW40 to reduce robust overfitting.
- Save four checkpoints (74/89/99/best).
- Source: Sec. 3.1, Table 1.

### Stage 3: Record rich diagnostics during training
- Per-epoch logs: AT loss/accuracy, validation clean/attack metrics.
- Additional diagnostics: stable accuracy and empirical Lipschitz constant.
- Source: Sec. 3.2, Eq. (1), Table 1.

### Stage 4: Final robustness evaluation
- Evaluate best checkpoint on test set with FGSM, PGD20, PGD-CW40, AA-Compact.
- Evaluate common corruptions on CIFAR-10-C.
- Source: Sec. 3.2, Sec. 4, Table 1.

### Stage 5: Reuse as NAS benchmark
- Run black-box NAS (Random, Local Search, RE, BANANAS) with max 500 queries.
- Compare best-found architecture metrics over 400 runs.
- Source: Sec. 5, Table 2.

## Pseudocode
```text
Algorithm: NARes Dataset Construction and NAS Reuse
Input:
  Search dimensions D={4,5,7,9,11}, W={8,10,12,14,16}
  Training data (CIFAR-10), validation data (CIFAR-10.1), attacks A
Output:
  Queryable robustness dataset R, optional NAS benchmark results B

1. Enumerate all architecture vectors v in D^3 x W^3 and instantiate WRN(v).
   Source: Sec. 3.1, Fig. 1
2. For each architecture a:
   Train with PGD adversarial training for 100 epochs with fixed hyperparameters.
   Source: Sec. 3.1
3. After each epoch:
   evaluate validation clean + PGD20 + PGD-CW40, plus stable accuracy and LIP.
   Source: Sec. 3.2, Eq. (1), Table 1
4. Select best epoch by validation PGD-CW40 and save checkpoints {74, 89, 99, best}.
   Source: Sec. 3.1, Table 1
5. Evaluate best checkpoint on test attacks (FGSM/PGD20/PGD-CW40/AA-Compact)
   and CIFAR-10-C corruption metrics; store all metrics in R.
   Source: Sec. 3.2, Sec. 4, Table 1
6. (Optional benchmark usage) Run NAS algorithms with <=500 queries and report
   best-found metrics over repeated runs.
   Source: Sec. 5, Table 2
```

## Training Pipeline
1. Enumerate WRN macro architectures.
2. Apply unified PGD adversarial training.
3. Track validation robust metrics each epoch.
4. Early-stop by validation PGD-CW40 and keep four checkpoints.
5. Aggregate full robustness metrics into dataset entries.

Sources:
- Sec. 3.1, Sec. 3.2, Table 1.

## Inference Pipeline
1. Query NARes by architecture vector (or sampled candidate).
2. Retrieve target metric(s): robust accuracy, stable accuracy, LIP, corruption scores.
3. Use queried results for ranking, correlation study, or black-box NAS simulation.

Sources:
- Sec. 4, Sec. 5, Table 2.

## Complexity and Efficiency
- Dataset construction cost:
  - Training: ~13.1K GPU days (~36 GPU years).
  - Evaluation: ~2.9K GPU days (~8 GPU years).
  - Total: ~44 GPU years (reported).
- Search-space size: 15,625 architectures.
- NAS benchmark query budget in paper: 500 (3.2% of search space).

## Implementation Notes
- Attack settings include `epsilon=8/255`; PGD20 uses step size `0.8/255`.
- Validation uses CIFAR-10.1 for model selection.
- Stable accuracy and empirical LIP are first-class diagnostics, not only side metrics.
- Model checkpoints at multiple milestones enable fine-tuning and longitudinal analysis.
- Official code release is stated as future/open-source intent in paper text, but no public repository link is present in the current public record.

## Comparison to Related Methods
- Compared with [[NADR-Dataset]]: NARes emphasizes WRN macro search space with larger-capacity models.
- Compared with [[NAS-Bench-201]]-style robust datasets: moves focus from cell topology to stage-level depth/width design.
- Compared with [[RobustBench]]: NARes is architecture-space exhaustive within a fixed macro design family.
- Main advantage: high-resolution robustness landscape with reproducible query workflow.
- Main tradeoff: confined to CIFAR-10 + WRN macro family and a single full sweep.

## Evidence and Traceability
- Key figure(s): Fig. 1-7.
- Key table(s): Table 1-2.
- Key equation(s): Eq. (1) (empirical LIP estimate).
- Key algorithm(s): Not explicitly named in main text; pipeline inferred from Sec. 3 and Table 1.

## References
- OpenReview: https://openreview.net/forum?id=AZVvTBxTdZ
- PDF: https://openreview.net/pdf/adb9acc706c4b858a6448cb218e58621b71dd419.pdf
- Supplementary: https://openreview.net/attachment?id=AZVvTBxTdZ&name=supplementary_material
- Code: Not publicly linked
- Local implementation: Not archived
