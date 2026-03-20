---
title: "ZCP-Eval"
type: method
source_paper: "An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness"
source_note: "[[ZCP-Eval]]"
authors: [Jovita Lukasik, Michael Moeller, Margret Keuper]
year: 2025
venue: IJCV
tags: [nas-method, nas, zero-cost-proxy, robustness, random-forest]
created: 2026-03-13
updated: 2026-03-20
---

# ZCP-Eval

## One-line Summary
> ZCP-Eval tests whether cheap zero-cost signals can predict robust architecture quality and shows robust targets require multi-feature fusion instead of a single proxy.

## Source
- Paper: [An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness](https://doi.org/10.1007/s11263-024-02265-7)
- arXiv: https://arxiv.org/abs/2307.09365
- Code: https://github.com/jovitalukasik/zcp_eval
- Paper note: [[ZCP-Eval]]

## Applicable Scenarios
- Problem type: Fast ranking/regression of architecture clean and robust accuracy before expensive full training.
- Assumptions: Candidate architectures lie in a benchmarked search space (here [[NAS-Bench-201]]) with available proxy features.
- Data regime: Offline supervised prediction with benchmark labels.
- Constraints: Robust evaluation budget is limited; need cheaper surrogate filtering.
- Why it fits: Random-forest regression over proxy vectors yields strong `R^2` under low training budgets.

## Not a Good Fit When
- You need guaranteed causal robustness estimates rather than empirical prediction.
- Target space/task is far from NAS-Bench-201 with no calibration set.
- Proxy feature extraction is inconsistent or unavailable.

## Inputs, Outputs, and Objective
- Inputs: Per-architecture proxy vector from 15 ZCPs (`jacov`, `nwot`, `snip`, `flops`, `params`, `jacob_fro`, etc.), optionally plus 191 [[Neural Graph Features (GRAF)]].
- Outputs: Predicted clean accuracy and/or attack-specific robust accuracy.
- Objective: Maximize prediction quality (`R^2`) for single-objective and multi-objective targets.
- Core assumptions: Proxy statistics encode enough architecture information to extrapolate clean and robust behavior.

## Method Breakdown
### Stage 1: Build architecture-feature table
- Collect ZCP values per architecture and align with robustness labels.
- Robustness labels come from Jung et al. 2023 and Wu et al. 2024 datasets.
- Source: Sec. 3, Sec. 4.1, Sec. 4.2, Sec. 4.3.

### Stage 2: Train random-forest predictors
- Train with sample sizes 32 / 128 / 1024.
- Run both single-target and multi-target settings.
- Source: Sec. 5.2, Table 1-7.

### Stage 3: Analyze feature utility
- Evaluate category-wise ablations (Jacobian, Pruning, Piecewise-linear, Hessian, Baselines, GRAF).
- Perform Top-1-only and Excluding-Top-1 controls.
- Source: Sec. 5.2.5, Sec. 5.3.1, Table 8-10, Fig. 4-11.

## Pseudocode
```text
Algorithm: ZCP-Eval
Input: Architecture set A, proxy extractors P, robustness labels Y
Output: Prediction metrics and feature-importance conclusions

1. For each architecture a in A, compute or load proxy vector x_a from P.
   Source: Sec. 3, Sec. 4.3
2. Build dataset D = {(x_a, y_a)} where y_a contains clean and robust targets.
   Source: Sec. 4.2, Sec. 4.3
3. For each train size n in {32, 128, 1024}, fit RandomForestRegressor on D_n.
   Source: Sec. 5.2
4. Evaluate test R^2 for single-objective and multi-objective targets.
   Source: Sec. 5.2, Table 1-7
5. Run category ablation + Top-1-only + Excluding-Top-1 studies.
   Source: Sec. 5.2.5, Sec. 5.3.1, Table 8-10
6. Conclude whether robust prediction is single-proxy or multi-proxy dominated.
   Source: Sec. 6
```

## Training Pipeline
1. Load robustness benchmark labels and precomputed ZCP files.
2. Convert architecture encodings into NAS-Bench-201 IDs and align targets.
3. Train random forests (`n_estimators=100`, `bootstrap=True`, `oob_score=True` in released code).
4. Evaluate test `R^2` and perform feature-importance analysis.

Sources:
- Paper: Sec. 5.2, Sec. 5.3
- Code evidence: `random_forest.py`, `robustness_dataset.py`

## Inference Pipeline
1. Compute proxy vector for a candidate architecture.
2. Feed the vector into trained random-forest model.
3. Get clean/robust score predictions and rank candidates.

Sources:
- Sec. 5.2
- Inference from source (deployment pipeline is not separately formalized in paper)

## Complexity and Efficiency
- Time complexity: Not reported analytically.
- Space complexity: Not reported analytically.
- Runtime characteristic: Much cheaper than full adversarial training + attack evaluation per architecture.
- Scaling trend: Larger training sample sizes generally improve `R^2`; robust targets remain harder than clean targets in Jung et al. setting.

## Implementation Notes
- Archived local code path: `D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness`.
- External datasets are required by default:
  - `robustness-data/`
  - `zcp_data/`
  - `robustness_dataset_zcp/`
- Paper reports permutation feature importance; current public script mainly uses MDI (`rf.feature_importances_`) for importance computation.
- This paper-code difference should be tracked when reproducing figure-level analyses.

## Comparison to Related Methods
- Compared with [[Surrogate Predictor]] methods: ZCP-Eval uses hand-crafted proxies + tree regressor, focusing on robustness transferability analysis.
- Compared with [[One-shot NAS]] robust methods: this is an evaluator/analysis framework, not an end-to-end robust search algorithm.
- Main advantage: clear empirical guidance on which proxy combinations transfer to robust prediction.
- Main tradeoff: benchmark-centric conclusions and dependency on precomputed datasets.

## Evidence and Traceability
- Key figures: Fig. 1-2 (correlations), Fig. 3 (pipeline), Fig. 4-11 (feature importance).
- Key tables: Table 1-10.
- Key equations: no new optimization objective; contribution is evaluation protocol and analysis.
- Key code evidence: `random_forest.py` lines showing RF hyperparameters and MDI importance implementation.

## References
- DOI: https://doi.org/10.1007/s11263-024-02265-7
- arXiv: https://arxiv.org/abs/2307.09365
- Code: https://github.com/jovitalukasik/zcp_eval
- Local implementation: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness
