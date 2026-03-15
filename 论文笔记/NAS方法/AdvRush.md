---
title: "AdvRush"
type: method
source_paper: "AdvRush: Searching for Adversarially Robust Neural Architectures"
source_note: "[[AdvRush]]"
authors: [Jisoo Mok, ByungMin Kim, Jihoon Park, Sungroh Yoon]
year: 2021
venue: ICCV
tags: [nas-method, robust-nas, differentiable-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# AdvRush

## One-line Summary
> AdvRush is a DARTS-style robust NAS method that injects an input-loss-landscape smoothness regularizer (`L_lambda`) into architecture updates after warm-up to search for more adversarially robust cells.

## Source
- Paper: [AdvRush: Searching for Adversarially Robust Neural Architectures](https://arxiv.org/abs/2108.01289)
- HTML: https://arxiv.org/html/2108.01289
- CVF: https://openaccess.thecvf.com/content/ICCV2021/html/Mok_AdvRush_Searching_for_Adversarially_Robust_Neural_Architectures_ICCV_2021_paper.html
- Supplement (local): `D:/PRO/essays/papers/AdvRush Searching for Adversarially Robust Neural Architectures Supplemental.pdf`
- Code: Not found from CVF/arXiv/supp links in this run
- Paper note: [[AdvRush]]

## Applicable Scenarios
- Problem type: Robust neural architecture search for image classification.
- Assumptions: Differentiable supernet and bilevel optimization are available (DARTS family setup).
- Data regime: Supervised vision datasets with adversarial training/evaluation.
- Scale / constraints: Moderate search budget; prefers reusing DARTS pipeline over heavy robust search redesign.
- Why it fits: Robustness pressure is introduced at architecture level, not only in final training.

## Not a Good Fit When
- You need search spaces that are fully discrete/non-differentiable.
- You require an officially maintained public codebase for strict reproducibility.
- You cannot afford Hessian-related regularization overhead in search.

## Inputs, Outputs, and Objective
- Inputs: Supernet weights `w`, architecture parameters `alpha`, train/val splits, warm-up epochs `E_warmup`, regularization weight `gamma`.
- Outputs: Discrete robust architecture derived from optimized `alpha`.
- Objective:
  - Weight update: minimize training loss.
  - Architecture update (after warm-up): minimize `L_val + gamma * L_lambda`.
- Core assumptions: Lower expected largest input-Hessian eigenvalue correlates with smoother landscape and better adversarial robustness.

## Method Breakdown

### Stage 1: DARTS Warm-up Search
- Jointly update `w` and `alpha` with vanilla DARTS objective.
- No smoothness penalty yet.
- Source: Supplement App. A1, Algorithm 1, lines 3-5.

### Stage 2: Smoothness-Regularized Architecture Update
- Keep weight update unchanged.
- Replace architecture objective with `L_val + gamma * L_lambda`.
- `L_lambda = E[lambda_max(H)]`, `H = ∇_x^2 l(f_A(x), y)`.
- Source: Main paper Sec. 3.2 Eq. (9)-(10); Supplement Algorithm 1, line 8.

### Stage 3: Discretization and Final Training
- Derive final normal/reduction cells from `alpha` using DARTS discretization.
- Stack cells into final network and perform standard/adversarial training for evaluation.
- Source: Supplement Algorithm 1 line 11; Main paper experimental protocol.

## Pseudocode
```text
Algorithm: AdvRush Search
Input: total epochs E, warm-up epochs E_warmup, regularization weight gamma
Output: final architecture A*

1. Initialize supernet f_super(w0, alpha0).
   Source: Supplement Alg. 1 line 1
2. For i = 1..E:
   Source: Supplement Alg. 1 line 2
3.   Update wi using train gradient of L_train(w, alpha) (SGD).
     Source: Supplement Alg. 1 line 4/7
4.   If i <= E_warmup:
       update alpha_i using grad of L_val(wi, alpha) (Adam).
     Else:
       update alpha_i using grad of [L_val(wi, alpha) + gamma * L_lambda] (Adam).
     Source: Supplement Alg. 1 line 5/8; Main Sec. 3.2 Eq. (9)-(10)
5. End for
6. Discretize alpha_E into final architecture A* by DARTS rule.
   Source: Supplement Alg. 1 line 11
```

## Training Pipeline
1. Define DARTS-like search space (8 operators).
2. Run warm-up search without smoothness penalty.
3. Activate smoothness regularization for architecture update.
4. Discretize architecture and train final model under standard/adversarial settings.

Sources:
- Main paper Sec. 3, Sec. 4
- Supplement App. A1 and Table A1

## Inference Pipeline
1. Use trained final architecture for standard prediction.
2. Report clean and robust accuracy under attacks (FGSM/PGD/C&W/AutoAttack variants).
3. Optionally evaluate robustness across datasets and PGD iteration budgets.

Sources:
- Main paper tables/figures
- Supplement Table A2/A5, Fig. A6

## Complexity and Efficiency
- Time complexity: Not provided in closed form.
- Space complexity: Not provided in closed form.
- Runtime characteristics: Search adds Hessian-smoothness term to architecture step; still structurally close to DARTS.
- Scaling notes: `gamma` controls robustness-accuracy trade-off; overly large `gamma` can hurt clean performance.

## Implementation Notes
- Search operations: zero, skip-connect, avg/max pool, sep conv 3x3/5x5, dil conv 3x3/5x5.
- Architecture update optimizer: Adam (search), weights via SGD.
- Typical adversarial-training hyperparameters:
  - momentum 0.9
  - weight decay 1e-4
  - CIFAR/SVHN 200 epochs, Tiny-ImageNet 90 epochs
- `L_lambda` is activated after warm-up (example in supplement uses activation around epoch 50 for visualization).
- Code status: no official repository URL was directly recoverable from the checked official pages.

## Comparison to Related Methods
- Compared with [[DARTS]]:
  AdvRush adds smoothness regularization in architecture update after warm-up.
- Compared with [[PDARTS]]:
  AdvRush reports stronger robust metrics under adversarial training/evaluation in supplement comparisons.
- Main advantage: small algorithmic modification with robust gains.
- Main tradeoff: depends on Hessian-eigenvalue proxy quality and extra compute.

## Evidence and Traceability
- Key figure(s): Main Fig. 2; Supplement Fig. A1/A2/A3/A6
- Key table(s): Main Table 2/3; Supplement Table A1/A2/A3/A5/A6
- Key equation(s): Main Eq. (9)-(10) and search objective in Sec. 3.2
- Key algorithm(s): Supplement Algorithm 1

## References
- arXiv: https://arxiv.org/abs/2108.01289
- HTML: https://arxiv.org/html/2108.01289
- CVF: https://openaccess.thecvf.com/content/ICCV2021/html/Mok_AdvRush_Searching_for_Adversarially_Robust_Neural_Architectures_ICCV_2021_paper.html
- Code: Not found
- Local implementation: Not archived
