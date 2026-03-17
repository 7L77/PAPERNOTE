---
title: "Wsr-NAS"
type: method
source_paper: "Neural Architecture Search for Wide Spectrum Adversarial Robustness"
source_note: "[[Wsr-NAS]]"
authors: [Zhi Cheng, Yanxi Li, Minjing Dong, Xiu Su, Shan You, Chang Xu]
year: 2023
venue: AAAI
tags: [nas-method, robust-nas, adversarial-robustness]
created: 2026-03-17
updated: 2026-03-17
---

# Wsr-NAS

## One-line Summary

> Wsr-NAS extends one-shot robust NAS from single-strength robustness to multi-strength robustness by combining an adversarial-noise generator (AN-Estimator) and a lightweight loss predictor (EWSS/VLE).

## Source

- Paper: [Neural Architecture Search for Wide Spectrum Adversarial Robustness](https://doi.org/10.1609/aaai.v37i1.25118)
- HTML: https://doi.org/10.1609/aaai.v37i1.25118
- Code: https://github.com/zhicheng2T0/Wsr-NAS
- Paper note: [[Wsr-NAS]]

## Applicable Scenarios

- Problem type: Robust NAS for image classifiers where robustness should hold across multiple perturbation strengths.
- Assumptions: A differentiable supernet search space is available and adversarial robustness can be approximated from multi-strength validation losses.
- Data regime: Supervised classification (paper search on CIFAR-10; transfer/retrain on CIFAR-10 and ImageNet).
- Scale / constraints: Useful when naive multi-strength adversarial validation is too expensive.
- Why it fits: Wsr-NAS separates expensive robust-signal acquisition (AN-Estimator) from architecture-gradient computation (VLE/EWSS).

## Not a Good Fit When

- You only care about one specific perturbation strength and can optimize it directly.
- You need certified robustness guarantees rather than empirical adversarial robustness.
- Your search space is not differentiable / one-shot compatible.

## Inputs, Outputs, and Objective

- Inputs: Supernet architecture parameters \(A\), train/validation splits, PGD attack settings, selected robust strengths.
- Outputs: Final cell architecture (WsrNet variants), plus retrained robust model.
- Objective: Minimize weighted combination of predicted clean and multi-strength adversarial validation losses.
- Core assumptions: VLE prediction quality is sufficient to guide architecture updates; generated adversarial noises are informative for search.

## Method Breakdown

### Stage 1: Warm-up Supernet and Memories

- Warm up sampled supernet architectures.
- Build memory for predictor/VLE and AE memory for AN-Estimator training.
- Source: Algorithm 1 lines 1-18; Sec. "Search Procedure".

### Stage 2: Build Multi-strength Adversarial Signals

- Generate exact adversarial noises on a few base strengths (\(N_1\)).
- Generate additional strengths (\(N_2\)) through AN-Estimator.
- Source: Sec. "Adversarial Noise Estimator", Eq. (3), Eq. (5), Eq. (7), Table 5.

### Stage 3: Predict Validation Loss Vector (EWSS)

- Train VLE to map architecture encoding to clean + multi-strength losses.
- Use memory \(M_v\) and MSE training.
- Source: Sec. "Efficient Wide Spectrum Searcher", Eq. (8), Eq. (9).

### Stage 4: Update Architecture with Robust Search Objective

- Optimize architecture parameters via weighted clean/robust objective.
- Balance global clean-vs-robust tradeoff (\(\alpha,\beta\)) and per-strength robust weights (\(\beta_i\)).
- Source: Eq. (10), Algorithm 1 line 24.

## Pseudocode

```text
Algorithm: Wsr-NAS
Input: supernet parameters A, train split Dt, val split Dv, strengths {eps_i}
Output: searched robust architecture

1. Warm up a population of sampled supernet architectures for one epoch each.
   Source: Alg.1 lines 2-5
2. Build AE memory M_a and validation memory M_v using adversarial training/evaluation.
   Source: Alg.1 lines 6-17
3. Train AN-Estimator on M_a to predict noises at target strengths.
   Source: Alg.1 line 10, Eq.(5), Sec. AN-Estimator
4. Train VLE on M_v to predict clean + adversarial validation losses.
   Source: Alg.1 line 18, Eq.(8)-(9)
5. For each search iteration:
   5.1 Sample architecture and adversarially train one epoch on Dt.
       Source: Alg.1 lines 20-21
   5.2 Refresh M_a, AN-Estimator, and M_v with exact + estimated multi-strength adversarial examples.
       Source: Alg.1 line 22; Sec. AN-Estimator; Inference from source code
   5.3 Update VLE and then update A using robust objective.
       Source: Alg.1 lines 23-24, Eq.(10)
6. Decode final architecture from optimized A.
   Source: Sec. Preliminaries; Inference from source
```

## Training Pipeline

1. Split CIFAR-10 train set into \(D_t\) and \(D_v\).
2. Warm-up supernet with Gumbel-sampled cells.
3. Build memories using clean + PGD adversarial validation losses.
4. Train AN-Estimator and VLE.
5. Alternate: model training, memory refresh, predictor training, architecture update.

Sources:

- Algorithm 1; Sec. "Search Procedure"; `search/robust_train_search_official.py`.

## Inference Pipeline

1. Use searched cell genotype to instantiate WsrNet.
2. Retrain with chosen robust training method (PGD/TRADES/Fast-AT in experiments).
3. Evaluate under clean and multiple attack strengths.

Sources:

- Sec. "Experiments"; Table 1/2/4; README retrain scripts.

## Complexity and Efficiency

- Time complexity: Not provided as closed-form.
- Space complexity: Not provided as closed-form.
- Runtime characteristics: Search under 6 strengths with full method reports ~3.6 GPU days; naive scaling is higher.
- Scaling notes: AN-Estimator lowers per-added-strength cost versus naive direct PGD generation.

## Implementation Notes

- Official search script uses `search/robust_train_search_official.py` with `search/script/search_pgd.sh`.
- Code uses two AN variants: `AN_estimator` and `AN_estimator_plus` (plus version for larger-strength setting).
- Search objective in code starts from `[1,[1,2,3,5,7,10]]` and is renormalized with balance `[0.8,0.2]`.
- Predictor is a multi-head LSTM estimator (clean + six epsilon heads) in `module/estimator/predictor2.py`.
- Paper/code alignment: paper describes generic \(N_1,N_2\) design; code provides concrete CIFAR-10 strengths and practical training loops.

## Comparison to Related Methods

- Compared with [[RobNet]]: Wsr-NAS optimizes robustness over broader perturbation spectrum, not only single-strength target.
- Compared with [[AdvRush]]: Wsr-NAS adds explicit adversarial-noise generation + loss-estimation modules for multi-strength search efficiency.
- Main advantage: Better average robustness across a range of strengths with manageable search cost.
- Main tradeoff: More moving parts (noise estimator + predictor + memories), increasing engineering complexity.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2.
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5, Table 6.
- Key equation(s): Eq. (1), Eq. (3), Eq. (5), Eq. (7), Eq. (8), Eq. (9), Eq. (10).
- Key algorithm(s): Algorithm 1.

## References

- arXiv: Not explicitly provided in paper metadata
- HTML: https://doi.org/10.1609/aaai.v37i1.25118
- Code: https://github.com/zhicheng2T0/Wsr-NAS
- Local implementation: D:/PRO/essays/code_depots/Neural architecture search for wide spectrum adversarial robustness

