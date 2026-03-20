---
title: "IBFS"
type: method
source_paper: "Revisiting Neural Networks for Few-Shot Learning: A Zero-Cost NAS Perspective"
source_note: "[[IBFS]]"
authors: [Haidong Kang]
year: 2025
venue: ICML
tags: [nas-method, few-shot-learning, zero-cost-proxy, information-bottleneck]
created: 2026-03-20
updated: 2026-03-20
---

# IBFS

## One-line Summary
> IBFS ranks candidate architectures for few-shot learning at initialization by an information-bottleneck-inspired entropy score over Jacobian spectra, avoiding expensive search-time training.

## Source
- Paper: [Revisiting Neural Networks for Few-Shot Learning: A Zero-Cost NAS Perspective](https://proceedings.mlr.press/v267/kang25e.html)
- HTML: https://openreview.net/forum?id=fNixzmprun
- Code: Not found on PMLR/OpenReview page at note time
- Paper note: [[IBFS]]

## Applicable Scenarios
- Problem type: Fast architecture search for few-shot image classification.
- Assumptions: Initialization-time Jacobian spectral entropy correlates with final converged accuracy.
- Data regime: Training-free scoring for search; few-shot supervised finetuning/evaluation downstream.
- Scale / constraints: Useful when search budget is seconds/minutes rather than GPU-days.
- Why it fits: Uses cheap initialization statistics and skips iterative search-stage training.

## Not a Good Fit When
- You require theorem guarantees under highly non-convex practical settings without strong assumptions.
- You need reproducible engineering details from official released code.
- Your task distribution is far from image FSL and Jacobian entropy may not correlate with target quality.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture `F_i`, random mini-batch `X`, initialized parameters `w_i`.
- Outputs: Scalar expressivity/ranking score per architecture.
- Objective: Rank architectures by predicted transfer quality for few-shot tasks while minimizing search cost.
- Core assumptions: First-order landscape information is sufficient for practical ranking in this setting.

## Method Breakdown
### Stage 1: First-order convergence perspective for FSL meta-learning
- Recast the MAML-style objective and show a first-order convergence view (Theorem 4.1).
- Source: Sec. 4, Eq. (3), App. A.

### Stage 2: IB-inspired score derivation
- Start from `I(R;X) - β I(R;Y)` and derive a tractable entropy-driven form for architecture scoring.
- Source: Sec. 4.1, Eq. (4)-(8).

### Stage 3: Jacobian spectral entropy scoring at initialization
- Build Jacobian matrix over batch gradients and compute entropy-style score from eigenvalue distribution.
- Source: Sec. 4.1, Eq. (9)-(10).

### Stage 4: Search once, then adapt to FSL tasks
- Use the top-ranked architecture for downstream few-shot protocols (reported with RFS-style training).
- Source: Sec. 5-6, Tab. 3.

## Pseudocode
```text
Algorithm: IBFS
Input: Search space A, initialized params {w_i}, mini-batch X, optional few-shot tasks T
Output: Ranked architectures and selected architecture a*

1. For each architecture F_i in A, compute Jacobian J_i from gradients on X.
   Source: Sec. 4.1, Eq. (9)
2. Compute eigenvalues {lambda_k} of J_i and entropy-like score S_i.
   Source: Sec. 4.1, Eq. (10)
3. Rank all architectures by S_i and choose top architecture a*.
   Source: Sec. 4.1 + Sec. 5.2
4. Train/evaluate a* on few-shot tasks with standard protocol.
   Source: Sec. 5.1, Sec. 6.1
```

## Training Pipeline
1. Sample candidate architectures from NAS-Bench-201/DARTS-like search spaces.
2. Compute IBFS score at initialization (no search-stage training loop).
3. Select top architecture.
4. Run downstream supervised/meta-learning training for FSL evaluation.

Sources:
- Sec. 5.1 (setup), Sec. 5.2/6.1 (results), Tab. 1-3.

## Inference Pipeline
1. Given a new search space/task family, score architectures with initialization Jacobian entropy.
2. Select architecture with highest score.
3. Deploy selected architecture in target training/evaluation pipeline.

Sources:
- Sec. 4.1, Sec. 6.

## Complexity and Efficiency
- Time complexity: Dominated by one-pass Jacobian construction + eigenspectrum computation per candidate.
- Space complexity: Jacobian/kernel matrix storage for current batch.
- Runtime characteristics: Reported search cost 3.82s on NAS-Bench-201 and 0.0042 GPU-days on ImageNet1k setting.
- Scaling notes: Empirically keeps strong ranking quality with very low search budget.

## Implementation Notes
- Architecture stack: 5 or 8 searched cells; reduction cells at 1/3 and 2/3 depth; initial channels 48.
- Downstream optimizer: SGD, momentum 0.9, weight decay 5e-4.
- Training schedules: miniImageNet 120 epochs; tieredImageNet 80 epochs.
- Hardware: mostly RTX 2080Ti, some A100 80G.
- Code provenance: paper cites prior codebases (TENAS/RFS) but does not provide an explicit official repo URL.

## Comparison to Related Methods
- Compared with [[NASWOT]]: IBFS reports much stronger ranking correlation for FSL-oriented search (reported KD 0.752 vs 0.422).
- Compared with [[MetaNTK-NAS]]: IBFS reports much lower search cost (0.1h vs 1.92h in Tab. 3 setting).
- Main advantage: Very low search-time cost with competitive or better accuracy.
- Main tradeoff: Relies on proxy correlation assumptions and lacks official code release.

## Evidence and Traceability
- Key figure(s): Fig. 3 (proxy-accuracy relation), Fig. 4 (Kendall stability), Fig. 7-8 (searched cells).
- Key table(s): Tab. 1 (NAS-Bench-201), Tab. 2 (ImageNet1k), Tab. 3 (FSL), Tab. 4 (AutoFormer).
- Key equation(s): Eq. (3) convergence bound; Eq. (4)-(8) IB derivation; Eq. (9)-(10) Jacobian entropy score.
- Key algorithm(s): No boxed algorithm in main text; pipeline reconstructed from Sec. 4-6.

## References
- arXiv: Not listed on the ICML/PMLR entry at note time
- HTML: https://openreview.net/forum?id=fNixzmprun
- Code: Not found on PMLR/OpenReview page at note time
- Local implementation: Not archived
