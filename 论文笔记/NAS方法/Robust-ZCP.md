---
title: "Robust-ZCP"
type: method
source_paper: "ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION"
source_note: "[[Robust-ZCP]]"
authors: [Yuqi Feng, Yuwei Ou, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICLR
tags: [nas-method, robustness, zero-cost-proxy]
created: 2026-03-15
updated: 2026-03-15
---

# Robust-ZCP

## One-line Summary
> Robust-ZCP ranks candidate architectures for adversarial robustness using only initialization-time statistics, by multiplying an NTK-derived term and an input-loss-landscape term.

## Source
- Paper: [ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION](https://openreview.net/forum?id=zHf7hOfeer)
- HTML: https://openreview.net/forum?id=zHf7hOfeer
- Code: https://github.com/fyqsama/Robust_ZCP
- Paper note: [[Robust-ZCP]]

## Applicable Scenarios
- Problem type: Cheap ranking of candidate architectures before expensive adversarial training.
- Assumptions: Initialization-level signals correlate with final adversarial accuracy.
- Data regime: Supervised image classification (CIFAR/ImageNet style).
- Scale / constraints: Large architecture pools where full robust training is too expensive.
- Why it fits: Score computation avoids explicit adversarial-example generation and full training.

## Not a Good Fit When
- You need certified robustness guarantees instead of empirical ranking.
- The task is far from the evaluated CNN search spaces and no calibration exists.
- The architecture family has strong training-dynamics effects not visible at initialization.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture, small data batches, initialization weights.
- Outputs: Scalar robustness proxy score `R` for ranking.
- Objective: Select architectures with high expected adversarial accuracy at very low search cost.
- Core assumptions: NTK and input-landscape surrogates at initialization preserve useful robustness ordering.

## Method Breakdown

### Stage 1: NTK surrogate term
- Compute a layer/sample averaged gradient-inner-product quantity to approximate the NTK-eigenvalue-related part (Eq. 8).
- Source: Sec. 3.2-3.3, Eq. (4), Eq. (8).

### Stage 2: Input landscape surrogate term
- Approximate the largest input-Hessian eigenvalue via finite difference:
  `|| (l(x + h z*) - l(x)) / h ||^2`, where `l(x)=grad_x L(theta0,x)`.
- Source: Sec. 3.2-3.3, Eq. (4), Eq. (7).

### Stage 3: Compose score and rank
- Multiply both terms with an exponential scaling and minus sign to get the final robust proxy score.
- Rank candidate architectures by score and keep top candidates.
- Source: Eq. (4), Sec. 4.1.2.

### Stage 4: Train selected architecture
- Adversarially train and evaluate only selected architectures under white-box/black-box attacks.
- Source: Sec. 4.1, Table 1-4.

## Pseudocode
```text
Algorithm: Robust-ZCP
Input: Candidate architectures A, sample set X, init weights theta0, hyperparameters M,N,h,t
Output: Ranked architectures by robust proxy score

1. For each architecture a in A, initialize weights theta0.
   Source: Sec. 3.2
2. Estimate NTK term:
   S_ntk = (1 / (M N^2)) * sum_m sum_i sum_j <df_theta0(x_i)/dtheta0^m, df_theta0(x_j)/dtheta0^m>.
   Source: Eq. (8)
3. Estimate landscape term:
   S_land = || (l(x + h z*) - l(x)) / h ||_2^2, with l(x)=grad_x L(theta0,x), z*=sign(grad_x L)/||sign(grad_x L)||.
   Source: Eq. (7)
4. Compute final score:
   R = -exp(t * S_ntk) * S_land.
   Source: Eq. (4)
5. Rank architectures by R and select top-K for full adversarial training/evaluation.
   Source: Sec. 4.1.2
6. (Code detail) Restrict sampled cells by specific structural filters (e.g., skip-connect count checks).
   Source: Inference from source (`search_robust.py`)
```

## Training Pipeline
1. Sample candidate architectures (paper: random sample 1,000 from DARTS space).
2. Compute Robust-ZCP score on initialization.
3. Choose best architecture(s) by score.
4. Adversarially train selected architecture(s) and report robustness metrics (FGSM/PGD/APGD/AA).

Sources:
- Sec. 4.1.1-4.1.2
- `exps/Robust_ZCP/search_robust.py`

## Inference Pipeline
1. Given a new candidate architecture, instantiate with random initialization.
2. Compute `R` via NTK surrogate + landscape surrogate.
3. Use `R` for ranking/pruning before expensive training.

Sources:
- Sec. 3.2-3.4
- Eq. (4), Eq. (7), Eq. (8)

## Complexity and Efficiency
- Time complexity: `O(MN^2)` (reported in paper).
- Space complexity: Not explicitly reported.
- Runtime characteristics: No adversarial-example generation during proxy scoring.
- Scaling notes: In experiments, search cost stays very low even in larger search spaces (0.017 -> 0.019 GPU days).

## Implementation Notes
- Core score code:
  - `functions.py::procedure` computes `RF = -exp(conv * 5000000) * regularizer_average`.
  - `regularizer.py::loss_cure.regularizer` computes the finite-difference landscape term.
- Practical hyperparameters:
  - Paper correlation setup: `M=11`, `N=25`, `h=50`, `t=5x10^6`, batch size 8.
  - Search script defaults differ (`batch_size_1=1`, `batch_size_2=32`) for scoring loops.
- Optimization tricks / constraints:
  - Candidate genotypes in code are filtered by skip-connection count in normal cell.
  - CIFAR path in released script may need local rewriting for reproduction.
- Failure modes / gotchas:
  - Initialization-only signal can mis-rank architectures that are hard to train but look good at init.

## Comparison to Related Methods
- Compared with CRoZe:
  - Robust-ZCP removes explicit adversarial-example generation in proxy stage.
- Compared with classic robust NAS (e.g., RACL/DSRNA):
  - Robust-ZCP is far cheaper for search, then uses full training only for selected candidates.
- Main advantage: Very low search cost with competitive robustness.
- Main tradeoff: Relies on approximations and initialization-level surrogates.

## Evidence and Traceability
- Key figure(s): Fig. 1-4.
- Key table(s): Table 1-6.
- Key equation(s): Eq. (4), Eq. (7), Eq. (8).
- Key algorithm(s): Proxy-based architecture ranking workflow (Sec. 4.1.2).

## References
- arXiv/OpenReview: https://openreview.net/forum?id=zHf7hOfeer
- HTML: https://openreview.net/forum?id=zHf7hOfeer
- Code: https://github.com/fyqsama/Robust_ZCP
- Local implementation: D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION
