---
title: "Dextr"
type: method
source_paper: "Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature"
source_note: "[[Dextr]]"
authors: [Rohan Asthana, Joschua Conrad, Maurits Ortmanns, Vasileios Belagiannis]
year: 2025
venue: TMLR
tags: [nas-method, zero-cost-proxy, training-free-nas, svd, curvature]
created: 2026-03-16
updated: 2026-03-16
---

# Dextr

## One-line Summary
> Dextr is a label-free zero-shot NAS proxy that combines inverse feature-map condition numbers and output extrinsic curvature to balance convergence/generalization and expressivity.

## Source
- Paper: [Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature](https://openreview.net/forum?id=X0vPof5DVh)
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- Code: https://github.com/rohanasthana/Dextr
- Paper note: [[Dextr]]

## Applicable Scenarios
- Problem type: training-free architecture ranking/search in CNN and ViT search spaces.
- Assumptions: layer features are available at initialization; output curvature can be estimated from synthetic curve inputs.
- Data regime: label-free (single input sample is sufficient in paper setup).
- Scale / constraints: suitable when candidate pool is large and full training per candidate is unaffordable.
- Why it fits: two complementary terms target both trainability (C/G) and expressivity.

## Not a Good Fit When
- You need direct latency-aware deployment optimization instead of accuracy-oriented proxy ranking.
- High-order autodiff for curvature is too expensive for your budget.
- Your architecture/data pipeline makes stable feature SVD extraction unreliable.

## Inputs, Outputs, and Objective
- Inputs: initialized network \(f\), one unlabeled image batch \(x\), synthetic curve input \(g(\theta)\).
- Outputs: scalar Dextr score per architecture.
- Objective: rank architectures by expected final performance before expensive training.
- Core assumptions: larger \(\sum_l 1/c_l(X_\phi)\) implies better C/G; larger \(\kappa(\theta)\) implies better expressivity.

## Method Breakdown

### Stage 1: Feature-map linear-independence scoring
- Collect intermediate layer outputs \(X_\phi\).
- Flatten each layer feature map matrix and compute singular values.
- Use inverse condition signal \(1/c_l(X_\phi)\).
- Source: Sec. 3.3.1-3.3.3, Eq. (8), Appendix A.6.

### Stage 2: Output-curve extrinsic curvature
- Build circular input trajectory \(g(\theta)\).
- Compute first/second derivatives of outputs w.r.t. \(\theta\), estimate curvature \(\kappa(\theta)\).
- Source: Sec. 3.2.2, Eq. (5), Eq. (8), Appendix A.6.

### Stage 3: Harmonic-style fusion
- Apply log transform to both terms and combine:
  \[
  \text{Dextr}=\frac{a\cdot b}{a+b},
  \quad
  a=\log\!\left(1+\sum_l\frac{1}{c_l(X_\phi)}\right),\;
  b=\log(1+\kappa(\theta))
  \]
- Source: Sec. 3.3.3, Eq. (8).

### Stage 4: Search usage
- Use Dextr as proxy criterion inside benchmark correlation pipelines or search loops (DARTS/AutoFormer).
- Source: Sec. 4.1-4.2, Table 1-3, Appendix A.7.

## Pseudocode
```text
Algorithm: Dextr Scoring
Input: Network f, unlabeled batch x, curve parameter grid theta
Output: Dextr score s

1. Forward once on x and record per-layer features X_phi,l.
   Source: Appendix A.6
2. For each layer l, reshape feature map matrix and compute SVD values.
   Source: Sec. 3.3.1-3.3.2
3. Compute C/G term a = log(1 + sum_l 1/c_l(X_phi,l)).
   Source: Sec. 3.3.3, Eq. (8)
4. Generate curve input g(theta), forward through f, compute derivatives wrt theta.
   Source: Sec. 3.2.2, Eq. (5), Appendix A.6
5. Compute expressivity term b = log(1 + kappa(theta)).
   Source: Sec. 3.2.2, Sec. 3.3.3
6. Return s = a*b/(a+b).
   Source: Sec. 3.3.3, Eq. (8)
```

## Training Pipeline
1. No per-architecture training required for scoring.
2. Initialize candidate architecture weights.
3. Compute Dextr score from one unlabeled sample + curve input.
4. Rank candidates and run search procedure.
5. Train only selected architecture(s) for final benchmark reporting.

Sources:
- Sec. 4.1-4.2, Appendix A.6-A.7.

## Inference Pipeline
1. Given a new candidate architecture, initialize weights.
2. Run Dextr scoring procedure.
3. Compare score against candidate pool.
4. Keep top-ranked architecture(s) for downstream full training/evaluation.

Sources:
- Sec. 4.1, Appendix A.6.

## Complexity and Efficiency
- Time complexity: not reported in closed form.
- Space complexity: not reported in closed form.
- Runtime characteristics: search cost reported as low as 0.07 GPU days on DARTS setting.
- Scaling notes: curvature estimation is the expensive part due higher-order gradients.

## Implementation Notes
- Local implementation:
  - `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`
  - `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr_utils/no_free_lunch_architectures/length.py`
- Code computes per-layer SVD ratio `min(s)/max(s)` (inverse condition signal).
- Score uses `log(1 + sum(layer_scores))`.
- Curvature computed by differentiating outputs wrt trajectory parameter \(\theta\).
- Final fusion in code matches Eq. (8): `results * curvature / (results + curvature)`.
- Practical caveat: if curvature fails (NaN/exception), code falls back to SVD-side term.

## Comparison to Related Methods
- Compared with [[MeCo]]: Dextr explicitly adds expressivity term via curvature.
- Compared with [[AZ-NAS]]: Dextr is simpler single-proxy fusion, while AZ-NAS is multi-proxy assembly.
- Main advantage: label-free and balanced signal design.
- Main tradeoff: curvature computation overhead and occasional instability on some search spaces (Appendix NATS-Bench-SSS case).

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2.
- Key table(s): Table 1, Table 2, Table 3, Table 4, Appendix Table 6-8.
- Key equation(s): Eq. (5), Eq. (7), Eq. (8), Appendix Eq. (22).
- Key algorithm(s): procedure described in Appendix A.6 (no formal algorithm block in main text).

## References
- arXiv: Not listed in official README (OpenReview version used)
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- Code: https://github.com/rohanasthana/Dextr
- Local implementation: D:/PRO/essays/code_depots/Dextr

