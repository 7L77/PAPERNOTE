---
title: "NAS-Bench-301"
type: method
source_paper: "NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH"
source_note: "[[NAS-Bench-301]]"
authors: [Julien Siems, Lucas Zimmer, Arber Zela, Jovita Lukasik, Margret Keuper, Frank Hutter]
year: 2020
venue: arXiv
tags: [nas-method, benchmark, surrogate-model, architecture-performance-prediction]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-Bench-301

## One-line Summary

> NAS-Bench-301 uses learned surrogate regressors to emulate expensive architecture training in the DARTS search space, enabling realistic and repeatable NAS benchmarking at a tiny fraction of the compute cost.

## Source

- Paper: [NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH](https://arxiv.org/abs/2008.09777)
- HTML: https://arxiv.org/html/2008.09777
- Code: https://github.com/automl/nasbench301
- Paper note: [[NAS-Bench-301]]

## Applicable Scenarios

- Problem type: Benchmarking and comparing NAS optimizers on large architecture spaces.
- Assumptions: Search space is fixed and encodable; enough architecture-performance samples are available to fit surrogates.
- Data regime: Offline supervised regression over architecture-performance pairs.
- Scale / constraints: Very large spaces where exhaustive tabulation is impossible (e.g., >10^18 architectures).
- Why it fits: Turns each expensive architecture training run into cheap surrogate queries while preserving optimizer ranking trends.

## Not a Good Fit When

- You need exact final performance for each architecture without model approximation error.
- The target search space/task distribution is far from the surrogate training data.
- The benchmark users can exploit surrogate internals (instead of black-box querying), causing benchmark overfitting.

## Inputs, Outputs, and Objective

- Inputs: Architecture encoding (DARTS cell graph/config), optional query settings (e.g., stochastic ensemble sample), and runtime features for runtime surrogate.
- Outputs: Predicted validation error/accuracy and predicted runtime for that architecture.
- Objective: Approximate true benchmark behavior so optimizer comparisons are realistic and cheap.
- Core assumptions: Similar architectures have learnable performance regularities, and sampled trajectories cover enough regions of the search space.

## Method Breakdown

### Stage 1: Build architecture-performance dataset

- Collect architecture evaluations from diverse optimizers (RS, DE, RE, TPE, BANANAS, COMBO, DARTS, GDAS, RANDOM-WS, PC-DARTS).
- Store architecture representation and validation/test/runtime targets.
- Source: Sec. 3, Table 2.

### Stage 2: Fit surrogate regressors

- Train multiple candidates (GIN, LGB, XGB, RF, SVR, etc.) with HPO.
- Evaluate fit with R2 and sparse Kendall tau (sKT).
- Source: Sec. 4.1-4.2, Table 3, Table 6.

### Stage 3: Validate out-of-trajectory generalization

- Perform leave-one-optimizer-out (LOOO): hold out one optimizer trajectory and test extrapolation.
- Use both R2 and sKT to assess quality on unseen optimizer regions.
- Source: Sec. 4.3, Table 4.

### Stage 4: Model noise and predictive distribution

- Train deep ensembles (10 base learners) for top surrogate families.
- Compare to repeated groundtruth evaluations via MAE and KL divergence.
- Source: Sec. 4.6, Table 5.

### Stage 5: Use as benchmark engine

- Replace true training-evaluation loop with surrogate query loop.
- Compare anytime trajectories against real benchmark to verify ranking consistency.
- Source: Sec. 5, Fig. 9-10.

## Pseudocode

```text
Algorithm: NAS-Bench-301 Surrogate Benchmark
Input: Search space Lambda (DARTS), collected evaluations D={(arch_i, y_i, t_i)}, optimizer O
Output: Surrogate-based anytime trajectory and final architecture ranking

1. Train surrogate candidates f_j on D to predict validation performance y.
   Source: Sec. 4.1-4.2
2. Select/report surrogate(s) using R2 + sparse Kendall tau + LOOO behavior.
   Source: Table 3, Table 4
3. Train runtime surrogate g on runtime targets t.
   Source: Sec. 5, Appendix A.6.1
4. Run optimizer O with black-box calls:
      query(arch) -> sample/estimate y_hat from surrogate ensemble,
                     estimate t_hat from runtime surrogate.
   Source: Sec. 5.1
5. Aggregate anytime best-so-far trajectory over repeated runs and compare against real benchmark trends.
   Source: Fig. 9, Fig. 10
6. Enforce benchmark protocol: do not search directly in surrogate latent/embedding space.
   Source: Sec. 6
```

## Training Pipeline

1. Encode architectures in DARTS search space to model-specific features (graph-based for GIN, tabular config for tree models).
2. Split train/val/test (and optimizer-aware splits for LOOO).
3. Run BOHB HPO for each surrogate family.
4. Fit final surrogates and evaluate R2/sKT/LOOO/distribution metrics.
5. Fit a separate LGB runtime model.

Sources:

- Sec. 4, Table 3-6
- Appendix A.2, A.6.1

## Inference Pipeline

1. Convert candidate architecture to benchmark input representation.
2. Query performance surrogate (or ensemble predictive distribution).
3. Query runtime surrogate.
4. Return predicted metric(s) to optimizer loop.

Sources:

- Sec. 5.1, Fig. 9
- Inference from source (API details are repository-driven)

## Complexity and Efficiency

- Time complexity: Not reported as closed-form.
- Space complexity: Not reported as closed-form.
- Runtime characteristics: Surrogate query is <1 second per architecture; real training is 1-2 hours per architecture.
- Scaling notes: Real benchmark comparison can require >10^7 seconds (~115 GPU days) for one trajectory, while surrogate enables repeated runs with error bars.

## Implementation Notes

- Official repo includes benchmark package/API and scripts for fitting surrogates.
- Pretrained model artifacts are versioned (v0.9, v1.0 in README links).
- Runtime model is trained separately from accuracy models.
- Paper emphasizes black-box usage to prevent surrogate overfitting by optimizer design.
- Paper-code caveat: benchmark quality is version-dependent; cross-paper comparisons should pin benchmark version.

## Comparison to Related Methods

- Compared with [[NAS-Bench-201]]: NAS-Bench-301 trades exact tabular lookup for scalable surrogate approximation on much larger spaces.
- Compared with [[Surrogate Predictor]] usage in search loops: NAS-Bench-301 elevates surrogate prediction into a standardized benchmark substrate.
- Main advantage: Realistic large-space benchmarking with strong speed/repeatability gains.
- Main tradeoff: Approximation error and data-coverage bias can affect optimizer ranking fidelity in some regimes.

## Evidence and Traceability

- Key figure(s): Fig. 2 (coverage), Fig. 7-8 (behavioral checks), Fig. 9-10 (anytime trajectory fidelity).
- Key table(s): Table 2 (data coverage), Table 3 (fit), Table 4 (LOOO), Table 5 (noise/distribution), Table 6 (HPO).
- Key equation(s): No single defining new equation; contribution is benchmark construction + evaluation protocol.
- Key algorithm(s): Surrogate fitting/evaluation protocol (Sec. 4-5).

## References

- arXiv: https://arxiv.org/abs/2008.09777
- HTML: https://arxiv.org/html/2008.09777
- Code: https://github.com/automl/nasbench301
- Local implementation: D:/PRO/essays/code_depots/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH
