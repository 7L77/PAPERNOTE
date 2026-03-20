---
title: "PWLNAS"
type: method
source_paper: "Loss Functions for Predictor-based Neural Architecture Search"
source_note: "[[PWLNAS]]"
authors: [Han Ji, Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICCV
tags: [nas-method, predictor-based-nas, ranking-loss, weighted-loss]
created: 2026-03-20
updated: 2026-03-20
---

# PWLNAS

## One-line Summary

> PWLNAS improves predictor-guided NAS by switching from warm-up losses (regression/ranking) to weighted losses as queried data grows, so the predictor first learns stable ordering and then focuses on top architectures.

## Source

- Paper: [Loss Functions for Predictor-based Neural Architecture Search](https://arxiv.org/abs/2506.05869)
- HTML: https://arxiv.org/html/2506.05869v1
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Ji_Loss_Functions_for_ICCV_2025_supplemental.pdf
- Code: https://github.com/jihan4431/PWLNAS
- Paper note: [[PWLNAS]]

## Applicable Scenarios

- Problem type: Predictor-based NAS with iterative querying under limited evaluation budget.
- Assumptions: Different loss families are better at different stages of queried-data scale.
- Data regime: Small to medium queried architecture set that grows over search iterations.
- Scale / constraints: Need better top-architecture hit rate without redesigning predictor backbone.
- Why it fits: Piecewise loss can be plugged into existing predictor-guided evolutionary loops.

## Not a Good Fit When

- Search loop cannot support staged retraining of the predictor.
- You have abundant full-supervision and can directly train high-fidelity predictors offline.
- Task/domain shift is extreme and warm-up/focus thresholds cannot be calibrated.

## Inputs, Outputs, and Objective

- Inputs: Search space \(S\), queried architecture-performance pairs \(D_t\), predictor \(f_\theta\), piecewise loss schedule.
- Outputs: Best architecture found under a fixed query budget.
- Objective: Improve top-ranking quality of predictor and therefore final searched architecture quality.
- Core assumptions: Ranking-style losses are better in data-scarce phase; weighted losses are better once enough queried data exists.

## Method Breakdown

### Stage 1: Warm-up predictor training

- Train predictor with regression or ranking loss to establish global/relative ordering.
- Typical warm-up choices: HR or ListMLE (task-dependent).
- Source: Sec. 4.3, Sec. 5, Supplementary Table 9.

### Stage 2: Loss switch to top-focused objective

- Once queried samples exceed a threshold, switch to weighted loss (MAPE/WARP/EW).
- Goal is to amplify discrimination among high-performing architectures.
- Source: Sec. 4.3, Sec. 5, Supplementary Table 9.

### Stage 3: Predictor-guided evolutionary search loop

- Score candidate architectures with predictor, sample promising ones, query true performance, and update \(D_t\).
- Retrain predictor repeatedly under piecewise loss schedule.
- Source: Sec. 4.3.

### Stage 4: Task-specific loss pairing

- NAS-Bench-201: HR -> MAPE.
- NAS-Bench-101: ListMLE -> WARP.
- TransNAS-Bench-101 Micro: Jigsaw uses MSE -> EW; other tasks use HR -> WARP.
- DARTS: HR -> MAPE.
- Source: Sec. 4.3, Supplementary Table 9.

## Pseudocode

```text
Algorithm: PWLNAS
Input: Search space S, predictor f_theta, query budget B, warm-up threshold q_w, losses (L_warm, L_focus)
Output: Best architecture x_best

1. Initialize queried set D with a small random architecture subset.
   Source: Sec. 4.3
2. while |D| < B:
   2.1 Train predictor f_theta on D with:
       if |D| <= q_w: use L_warm
       else: use L_focus
       Source: Sec. 4.3; Supplementary Table 9
   2.2 Score candidate pool C by f_theta and select promising architectures.
       Source: Sec. 4.3
   2.3 Apply predictor-guided evolutionary sampling to propose new candidates.
       Source: Sec. 4.3
   2.4 Query true performance for selected candidates and add to D.
       Source: Sec. 4.3
3. Return the best architecture found in D.
   Source: Sec. 4.3
```

Inference from source:
- Exact candidate-pool construction and mutation/crossover hyperparameters are not fully listed in the released code; the loop above follows the paper-described predictor-guided evolutionary protocol.

## Training Pipeline

1. Choose predictor backbone (e.g., GCN in main comparisons).
2. Train predictor on queried architectures using warm-up loss.
3. Switch to weighted loss after warm-up threshold.
4. Refit predictor repeatedly during iterative querying.
5. Evaluate with top-ranking metrics and final searched architecture performance.

Sources:

- Sec. 4.1-4.3, Sec. 5, Supplementary Table 9.

## Inference Pipeline

1. Encode candidate architectures and feed into trained predictor.
2. Rank candidates by predicted scores.
3. Select top candidates for expensive true-performance query.
4. Update current best architecture under budget.

Sources:

- Sec. 4.3.

## Complexity and Efficiency

- Time complexity: Dominated by repeated predictor training + true-performance queries during search.
- Space complexity: Predictor parameters plus queried architecture cache.
- Runtime characteristics: Reported DARTS search cost around 0.2 GPU-days for PWLNAS setting (Table 5).
- Scaling notes: Benefit is strongest when query budget is limited and top-ranking quality dominates final search success.

## Implementation Notes

- Official repo currently exposes predictor model and loss implementations (`model.py`, `utils.py`) and dataset adapters.
- `utils.py` contains implementations for ListMLE, LR-style pair loss, WARP, EW, MAPE, and SR-related components.
- README states full ranking/search experiment code release is still pending.
- Practical takeaway: method-level strategy is paper-complete, while code-level end-to-end search scripts are partially released.

## Comparison to Related Methods

- Compared with fixed-loss predictors (e.g., MSE-only NPENAS-style setting): PWLNAS adapts loss to search stage.
- Compared with single ranking losses (HR/ListMLE): PWLNAS keeps early ranking strength but improves later top-hit precision.
- Main advantage: Better tradeoff between global ordering and top-architecture discovery.
- Main tradeoff: Requires a task-specific warm-up threshold and loss pair.

## Evidence and Traceability

- Key figure(s): Fig. 2, Fig. 3, Fig. 7.
- Key table(s): Table 2/3/4/5 in main paper, Table 9 in supplementary.
- Key equation(s): Loss definitions in Sec. 3 and Supplementary A.1-A.7.
- Key algorithm(s): Predictor-guided evolutionary search with piecewise loss in Sec. 4.3.

## References

- arXiv: https://arxiv.org/abs/2506.05869
- HTML: https://arxiv.org/html/2506.05869v1
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Ji_Loss_Functions_for_ICCV_2025_supplemental.pdf
- Code: https://github.com/jihan4431/PWLNAS
- Local implementation: D:/PRO/essays/code_depots/Loss Functions for Predictor-based Neural Architecture Search
