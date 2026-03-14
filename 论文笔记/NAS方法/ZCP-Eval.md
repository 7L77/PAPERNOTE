---
title: "ZCP-Eval"
type: method
source_paper: "An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness"
source_note: "[[ZCP-Eval]]"
authors: [Jovita Lukasik, Michael Moeller, Margret Keuper]
year: 2025
venue: IJCV
tags: [nco-method, nas, zero-cost-proxy, robustness]
created: 2026-03-13
updated: 2026-03-13
---

# ZCP-Eval

## One-line Summary
> ZCP-Eval studies whether cheap pre-training signals (ZCPs) can predict both clean and robust architecture performance, and finds robust prediction needs multi-feature fusion rather than a single proxy.

## Source
- Paper: [An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness](https://doi.org/10.1007/s11263-024-02265-7)
- HTML: https://link.springer.com/article/10.1007/s11263-024-02265-7
- Code: https://github.com/jovitalukasik/zcp_eval
- Paper note: [[ZCP-Eval]]

## Applicable Scenarios
- Problem type: Predict architecture clean/robust accuracy without full retraining.
- Assumptions: Search space is fixed and benchmarked (e.g., [[NAS-Bench-201]]), with available proxy computations.
- Data regime: Offline, supervised benchmark analysis.
- Scale / constraints: Thousands of architectures where full adversarial evaluation is expensive.
- Why it fits: Random-forest regression maps proxy vectors to robustness targets with good empirical R2.

## Not a Good Fit When
- You need guaranteed causal robustness estimates from first principles.
- Search space or task is far from NAS-Bench-201 distribution and no calibration data exists.
- No proxy values can be computed consistently across candidate architectures.

## Inputs, Outputs, and Objective
- Inputs: Per-architecture proxy vector (`jacov`, `nwot`, `snip`, `flops`, `params`, `jacob_fro`, optional GRAF features).
- Outputs: Predicted clean accuracy and/or attack-specific robust accuracy.
- Objective: Maximize prediction quality (R2) for single-objective and multi-objective targets.
- Core assumptions: Proxy statistics carry enough signal about final architecture behavior.

## Method Breakdown

### Stage 1: Build proxy-feature table
- Collect ZCP values for each architecture in NAS-Bench-201 and align with robustness labels.
- Merge robust attack metrics from Jung et al. 2023 / Wu et al. 2024 datasets.
- Source: Sec. 3, Sec. 4.1, Sec. 4.2, Sec. 4.3.

### Stage 2: Train prediction model
- Train random forest regressors with train sizes 32 / 128 / 1024.
- Run both single-target and multi-target prediction settings.
- Source: Sec. 5.2, Fig. 3, Table 1-5.

### Stage 3: Analyze feature utility
- Evaluate category ablations (Jacobian, Pruning, Baseline, Hessian, Piecewise-linear, GRAF).
- Compute feature importance and Top-1 / Excluding-Top-1 controls.
- Source: Sec. 5.2.5, Sec. 5.3, Table 8-10, Fig. 4-11.

## Pseudocode
```text
Algorithm: ZCP-Eval
Input: Architecture set A in NAS-Bench-201, proxy extractors P, robustness labels Y
Output: Prediction metrics and feature-importance analysis

1. For each architecture a in A, compute/collect proxy vector x_a from P.
   Source: Sec. 3, Sec. 4.3
2. Build dataset D = {(x_a, y_a)} for clean and robust targets.
   Source: Sec. 4.2, Sec. 4.3
3. For each train size n in {32, 128, 1024}, train random forest on D_n.
   Source: Sec. 5.2
4. Evaluate R2 on single objective and multi-objective targets.
   Source: Sec. 5.2, Table 1-5
5. Run feature analyses: category-only, Top-1-only, and remove-Top-1.
   Source: Sec. 5.2.5, Sec. 5.3.1, Table 8-10
6. Report robustness-specific conclusion: robust prediction requires multi-feature combination.
   Source: Sec. 6
```

## Training Pipeline
1. Load benchmark metadata + proxy files.
2. Convert architecture encodings to NAS-Bench-201 IDs and align labels.
3. Train `RandomForestRegressor` (100 trees, bootstrap, OOB enabled in released code).
4. Evaluate test R2 and inspect feature contributions.

Sources:
- Sec. 5.2, Sec. 5.3
- `random_forest.py` in archived repo

## Inference Pipeline
1. Compute proxy vector for a new candidate architecture.
2. Feed vector into trained random forest.
3. Obtain predicted clean/robust scores and rank candidates.

Sources:
- Sec. 5.2
- Inference from source (explicit serving pipeline is not separately formalized in paper)

## Complexity and Efficiency
- Time complexity: Not reported analytically.
- Space complexity: Not reported analytically.
- Runtime characteristics: Much cheaper than training all architectures under adversarial attacks.
- Scaling notes: Larger train size improves R2; robust objectives remain harder than clean objectives.

## Implementation Notes
- Architecture conversion and label alignment are coded in `random_forest.py` and `robustness_dataset.py`.
- External data dependencies are required (`robustness-data`, `zcp_data`, `robustness_dataset_zcp`).
- Released code shows MDI feature importance (`rf.feature_importances_`).
- Paper discussion emphasizes permutation importance; this is a paper-code mismatch to track explicitly.
- Practical gotcha: Without exact benchmark dumps, reproducing all paper tables is difficult.

## Comparison to Related Methods
- Compared with [[Surrogate Predictor]]: ZCP-Eval uses hand-crafted zero-cost features + tree regression, not learned black-box surrogates.
- Compared with [[One-shot NAS]]: This work is evaluator-focused (prediction/analysis), not a standalone weight-sharing search algorithm.
- Main advantage: Clear empirical map of which proxies transfer to robustness targets.
- Main tradeoff: Conclusions are benchmark-centric and rely on available precomputed data.

## Evidence and Traceability
- Key figure(s): Fig. 1-2 (correlation), Fig. 3 (pipeline), Fig. 4-11 (importance).
- Key table(s): Table 1-10.
- Key equation(s): Not method-defining; contribution is experimental evaluation protocol.
- Key algorithm(s): Random forest regression workflow (Sec. 5.2).

## References
- arXiv: https://arxiv.org/abs/2307.09365
- HTML: https://link.springer.com/article/10.1007/s11263-024-02265-7
- Code: https://github.com/jovitalukasik/zcp_eval
- Local implementation: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness

