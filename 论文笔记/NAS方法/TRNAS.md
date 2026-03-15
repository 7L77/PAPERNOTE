---
title: "TRNAS"
type: method
source_paper: "TRNAS: A Training-Free Robust Neural Architecture Search"
source_note: "[[TRNAS]]"
authors: [Shudong Yang, Xiaoxing Wang, Jiawei Ding, Yanyi Zhang, En Wang]
year: 2025
venue: ICCV
tags: [nas-method, robust-nas, training-free-nas, zero-cost-proxy]
created: 2026-03-15
updated: 2026-03-15
---

# TRNAS

## One-line Summary

> TRNAS uses a training-free robustness proxy (`R-Score`) plus multi-objective evolutionary selection to quickly find robust DNN architectures before expensive adversarial training.

## Source

- Paper: [TRNAS: A Training-Free Robust Neural Architecture Search](https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html)
- HTML: https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html
- Supplement: `D:/PRO/essays/papers/Yang_TRNAS_A_Training-Free_ICCV_2025_supplemental.pdf`
- Code: Not found (no official repository linked in paper/supplement as of 2026-03-15)
- Paper note: [[TRNAS]]

## Applicable Scenarios

- Problem type: robust neural architecture search under adversarial attacks.
- Assumptions: initialization-time proxy can rank architectures by robustness potential.
- Data regime: image classification (CIFAR-10/100, Tiny-ImageNet), cell-based search space.
- Scale / constraints: useful when full adversarial training for all candidates is too expensive.
- Why it fits: it decouples cheap pre-training ranking from expensive final adversarial training.

## Not a Good Fit When

- You need a method with publicly available reference code for immediate deployment.
- Your search space is not DARTS-like and proxy behavior is unknown.
- Robustness target differs strongly from FGSM/PGD/AutoAttack style perturbations.

## Inputs, Outputs, and Objective

- Inputs: candidate architectures in DARTS search space, calibration data batch, resource metrics (Params/FLOPs).
- Outputs: ranked architectures, selected Pareto candidates, final best robust architecture.
- Objective: maximize robust accuracy while controlling model size and compute.
- Core assumptions: higher `R-Score` correlates with better adversarial robustness after training.

## Method Breakdown

### Stage 1: Compute R-Score for Candidate Architectures

- Evaluate linear activation capability and feature consistency on untrained networks.
- Combine them into a single robustness proxy score.
- Source: Sec. 3.1, Eq. (2)-(7).

### Stage 2: Multi-objective Selection (MOS)

- Use clustering-based Pareto selection to preserve diversity and avoid premature convergence.
- Source: Sec. 3.2, Fig. 3.

### Stage 3: Evolutionary Search with Proxy Guidance

- Run evolutionary updates using `R-Score`-guided candidate filtering and selection.
- Source: Sec. 4.1; Supplement Sec. 3.2 (20 updates, parent/offspring size 50).

### Stage 4: Final Adversarial Training and Evaluation

- Fully train selected best architecture with PGD adversarial training.
- Evaluate with FGSM/PGD/AutoAttack.
- Source: Sec. 4.2; Supplement Sec. 3.2.

## Pseudocode

```text
Algorithm: TRNAS
Input: Search space S, update rounds T, population size N
Output: Best robust architecture a*

1. Initialize population P from search space S.
   Source: Sec. 4.1
2. For each architecture a in P, compute R-Score:
   R(a) = beta * LAM(a) + (1-beta) * FRM(a).
   Source: Sec. 3.1, Eq. (2)-(7)
3. Perform multi-objective selection with clustering-based Pareto strategy.
   Source: Sec. 3.2, Fig. 3
4. Generate offspring and iterate evolutionary updates for T rounds.
   Source: Sec. 4.1; Supplement Sec. 3.2
5. Select top candidate(s) and run adversarial training to convergence.
   Source: Sec. 4.2; Supplement Sec. 3.2
6. Return architecture with best robust metrics under FGSM/PGD/AutoAttack.
   Source: Sec. 4.2; Supplement Sec. 3.2
```

## Training Pipeline

1. Search stage: proxy-based evolutionary search in DARTS space.
2. Prune obviously poor operations before full search budget (supplement reports early pruning evaluations).
3. Train selected architecture via 7-step PGD adversarial training.
4. Use SGD with schedule settings from supplementary section.

Sources:

- Sec. 4.1, Sec. 4.2
- Supplement Sec. 2.2, Sec. 3.2

## Inference Pipeline

1. Use searched architecture and trained weights.
2. Report clean and attacked accuracy under predefined attack budgets.
3. Compare against robust NAS baselines on same benchmarks.

Sources:

- Sec. 4.2
- Supplement Sec. 3.2

## Complexity and Efficiency

- Time complexity: not provided in closed form.
- Space complexity: not provided in closed form.
- Runtime characteristics: supplementary reports about `0.02 GPU-days` for effective 1000 evaluations on RobustBench setup and up to `0.01 GPU-days` with multi-process optimization.
- Scaling notes: proxy inference is much cheaper than weight-sharing robust NAS; full adversarial training still dominates final cost.

## Implementation Notes

- Search space: 8 stacked cells in search stage, 20 stacked cells in final training.
- Evolutionary setup: 20 updates, parent size 50, offspring size 50, clustering size `e=20`.
- Attacks: FGSM (`8/255`), PGD (`2/255` step, 20/100 steps), AutoAttack (`8/255` budget).
- Hardware: single RTX 4090, PyTorch 2.0.
- Code availability: no official repository identified from paper and supplement.

## Comparison to Related Methods

- Compared with ZCPRob: TRNAS has better efficiency/coverage in supplementary efficiency analysis.
- Compared with [[CRoZe]]: TRNAS provides finer architecture discrimination in supplementary prediction-error plots.
- Compared with standard NAS (e.g., [[SWAP-NAS]], PADA, DARTS): TRNAS targets robust objective directly and performs better under attacks.
- Main advantage: robust ranking with low search cost.
- Main tradeoff: reproducibility risk due to missing official code.

## Evidence and Traceability

- Key figure(s): Fig. 2, Fig. 3 (main); Fig. 1 in supplement.
- Key table(s): Table 2/3/4 (main); Table 1/2/3/4 (supplement).
- Key equation(s): Eq. (2)-(7) for R-Score.
- Key algorithm(s): evolutionary + MOS search flow in Sec. 3.2 and Sec. 4.1.

## References

- arXiv/OpenAccess: https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html
- Supplement PDF: D:/PRO/essays/papers/Yang_TRNAS_A_Training-Free_ICCV_2025_supplemental.pdf
- Code: Not found
- Local implementation: Not archived
