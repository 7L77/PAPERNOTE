---
title: "NEAR"
type: method
source_paper: "NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance"
source_note: "[[NEAR]]"
authors: [Raphael T. Husistein, Markus Reiher, Marco Eckhoff]
year: 2025
venue: ICLR
tags: [nas-method, nas, training-free, zero-cost-proxy, effective-rank]
created: 2026-03-14
updated: 2026-03-14
---

# NEAR

## One-line Summary
> NEAR ranks untrained models by summing the [[Effective Rank]] of layer-wise pre/post activations, providing a broadly effective training-free architecture quality signal.

## Source
- Paper: [NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance](https://arxiv.org/abs/2408.08776)
- HTML: https://arxiv.org/html/2408.08776
- Code: https://github.com/ReiherGroup/NEAR
- Paper note: [[NEAR]]

## Applicable Scenarios
- Problem type: training-free architecture ranking and model pre-selection.
- Assumptions: random-input activation geometry correlates with final performance.
- Data regime: classification-heavy NAS benchmarks, plus tested transfer settings.
- Constraints: works when labels are missing and quick screening is needed.

## Not a Good Fit When
- You need precise ordering among very close top candidates.
- Optimization dynamics dominate performance differences.
- Hardware latency dominates objective and cannot be proxied by representational geometry.

## Inputs, Outputs, and Objective
- Inputs: model architecture, sampled inputs via dataloader, repetitions count.
- Outputs: scalar NEAR score.
- Objective: maximize correlation between proxy score and final model accuracy.
- Core assumption: better-balanced activation geometry implies stronger downstream trainability/accuracy.

## Method Breakdown

### Stage 1: Build Activation Matrices
- For each layer, construct pre-activation matrix `Z_l` and post-activation matrix `H_l` from sampled inputs.
- Source: Sec. 3.1-3.2

### Stage 2: Compute Effective Rank
- Use SVD singular values `\sigma_k`, normalize into `p_k`, then compute:
  `erank(A) = exp(-sum_k p_k log p_k)`.
- Source: Eq. (4), Eq. (5)

### Stage 3: Aggregate Layer Scores
- Compute:
  `s_NEAR = sum_l [ erank(Z_l) + erank(H_l) ]`.
- Source: Definition 3.2, Sec. 3.2

### Stage 4: Repeat and Average
- Repeat scoring with re-initialization / random sampling and average for stability.
- Source: Sec. 3.2 (stability recommendation), code `get_near_score(...)`

### Stage 5: CNN Efficiency Adaptation
- Reshape conv feature maps into matrices and use submatrix sampling for tractability.
- Source: Sec. 3.3

## Pseudocode
```text
Algorithm: NEAR Scoring
Input: Model F, input dataloader D, repetitions R
Output: Average NEAR score s

1. scores <- []
2. Repeat r = 1..R:
   2.1 For each relevant layer l, collect activation outputs over sampled inputs.
       Source: Sec. 3.2; code hook collection in near_score.py
   2.2 Build matrix representations (with CNN reshape/subsample if needed).
       Source: Sec. 3.3
   2.3 Compute erank for each pre/post activation matrix.
       Source: Eq. (4)-(5)
   2.4 Sum layer-wise eranks to get s_r.
       Source: Definition 3.2
   2.5 Reinitialize model parameters for next repetition.
       Source: code __reset_weights; Inference from source
3. Return mean(scores).
   Source: code get_near_score(...)
```

## Training Pipeline
1. No full training is required for scoring.
2. Run forward passes on sampled inputs only, compute NEAR, rank candidates.
3. Select top candidate(s) for downstream full training.

Sources:
- Sec. 1, Sec. 4.1
- Source: Inference from source

## Inference Pipeline
1. Choose architecture by NEAR ranking.
2. Train selected architecture with standard recipe.
3. Evaluate with standard inference on task metric.

Sources:
- Sec. 4
- Source: Inference from source

## Complexity and Efficiency
- Closed-form complexity: not explicitly reported.
- Dominant cost: repeated SVD on activation matrices.
- Practical efficiency: no backward pass or labels required; much cheaper than full NAS training loops.
- CNN case: matrix subsampling controls rank-computation overhead.

## Implementation Notes (Code-verified)
- Effective rank implementation: `src/near_score/near_score.py:get_effective_rank`.
- Layer collection uses forward hooks over weighted layers and activation modules.
- Conv outputs are transposed + flattened before submatrix truncation.
- Score averaging and model reinitialization are handled in `get_near_score`.
- Layer-size estimation function:
  `estimate_layer_size(models, sizes, dataloader, layer_index, slope_threshold, repetitions)`.

## Comparison to Related Methods
- Compared to ReLU-restricted proxies, NEAR supports broader activation choices.
- Compared to label-requiring gradient proxies, NEAR is label-free.
- Compared to single-space strong baselines, NEAR tends to show stronger cross-space consistency.

## Evidence and Traceability
- Key sections: Sec. 3.2, Sec. 3.3, Sec. 4
- Key equations: Eq. (4), Eq. (5), Definition 3.2 formula
- Key tables: Table 1, Table 2, Table 3, Table 4, Table 7, Table 8
- Key code paths:
  `src/near_score/near_score.py`, `example.py`

## References
- arXiv: https://arxiv.org/abs/2408.08776
- HTML: https://arxiv.org/html/2408.08776
- Code: https://github.com/ReiherGroup/NEAR
- Local implementation: D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance

