---
title: "PO-NAS"
type: method
source_paper: "Per-Architecture Training-Free Metric Optimization for Neural Architecture Search"
source_note: "[[PO-NAS]]"
authors: [Anonymous Author(s)]
year: 2025
venue: "NeurIPS 2025 (under review submission)"
tags: [nas-method, nas, training-free, zero-cost-proxy, surrogate-model, evolutionary-search]
created: 2026-03-16
updated: 2026-03-16
---

# PO-NAS

## One-line Summary
> PO-NAS learns architecture-specific weights over multiple training-free metrics with a cross-attention surrogate, then runs BO + evolution to find high-performing architectures under limited true-training budget.

## Source
- Paper: [Per-Architecture Training-Free Metric Optimization for Neural Architecture Search](D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf)
- HTML: Not provided in paper
- Code: https://anonymous.4open.science/r/PO-NAS-2953 (not clonable on 2026-03-16)
- Paper note: [[PO-NAS]]

## Applicable Scenarios
- Problem type: NAS in medium-to-large search spaces with expensive full-training evaluation.
- Assumptions: Multiple training-free metrics have complementary but architecture-dependent utility.
- Data regime: Small number of real-trained architectures + large pool of cheaply scored candidates.
- Scale / constraints: Designed to work even when only limited real evaluations are affordable.
- Why it fits: Uses per-architecture metric fusion and iterative feedback instead of fixed global metric weighting.

## Not a Good Fit When
- You cannot afford any real training feedback rounds.
- Search space encoding is unreliable, weakening the architecture embedding.
- Surrogate instability is unacceptable for the deployment setting.

## Inputs, Outputs, and Objective
- Inputs: Candidate architectures \(A\), architecture graph \(G(A)\), training-free metrics \(Z(A)\), sparse true performance labels \(f(A)\).
- Outputs: Best architecture \(A^*\); surrogate score \(\hat S(A)\) for ranking.
- Objective: Improve ranking consistency between surrogate scores and true performance while keeping search cost low.
- Core assumptions: Architecture-conditioned metric fusion improves transfer across tasks/spaces versus global fusion.

## Method Breakdown
### Stage 1: Initialization and pretraining
- Randomly sample initial architecture pool and compute real training-free metrics.
- Train initial subset for true performance labels.
- Pretrain architecture encoder + metric predictor with node-mask reconstruction and metric prediction losses.
- Source: Algorithm 1 lines 1-10, Sec. 3.2-3.3, Eq. (3)-(4).

### Stage 2: Surrogate BO loop
- Update surrogate on accumulated true-labeled set.
- Generate architecture-specific metric weights using cross-attention + MLP.
- Score/rank candidates and select top architecture for real training feedback.
- Source: Algorithm 1 lines 11-29, Sec. 3.4, Eq. (5)-(8).

### Stage 3: Evolutionary expansion (large-space mode)
- Select excellent architecture pairs via pair score combining operation cost and predicted fitness.
- Generate offspring using shortest-operation-path crossover + neighborhood mutation.
- Re-score offspring and refresh candidate pool.
- Source: Algorithm 1 lines 15-21, Sec. 3.5, Appendix A.2-A.4, Eq. (9), Algorithm 2.

## Pseudocode
```text
Algorithm: PO-NAS
Input: Candidate pool size N_ini, initial trained size N_t, pretrain epochs T_p, BO budget T_s, evolution start T_e, metrics Z
Output: Best architecture A*

1. Sample A0 with N_ini architectures; compute Z(A0).
   Source: Alg. 1 lines 1-3
2. Train N_t architectures from A0 to get Q0={(A, f(A))}.
   Source: Alg. 1 line 4
3. Pretrain encoder E and metric predictor Pz with L_recon + L_metric.
   Source: Alg. 1 lines 5-10; Sec. 3.3 Eq. (3)-(4)
4. For t = 1..T_s:
   4.1 Update surrogate M using Qt-1 with L_align + L_corr + L_dir.
       Source: Alg. 1 line 13; Sec. 3.4 Eq. (6)-(8)
   4.2 If t > T_e, run evolution:
       - choose elite set A_ex by M(E(A), Z)
       - choose parent pairs by S_pair = N*S_cost + (1-N)*S_pre
       - apply shortest-path crossover + neighborhood mutation to get offspring
       - keep strong offspring and update pool
       Source: Alg. 1 lines 15-21; Appendix A.3-A.4 Eq. (9); Alg. 2
   4.3 Select current best A_best by surrogate score and obtain true f(A_best).
       Source: Alg. 1 lines 23-28
   4.4 Add (A_best, f(A_best)) into Qt.
       Source: Alg. 1 line 28
5. Return architecture with best observed true performance in Q_Ts.
   Source: Alg. 1 line 30
```

## Training Pipeline
1. Precompute training-free metrics for initial candidate pool.
2. Pretrain GAT encoder + metric predictor.
3. Enter BO iterations; each round trains surrogate, selects/evaluates one best architecture by true training.
4. In larger spaces, add evolution-generated offspring and continue BO updates.

Sources:
- Sec. 3.2-3.5, Algorithm 1, Appendix B.2.

## Inference Pipeline
1. Use trained surrogate to quickly rank candidate architectures during search.
2. For final deployment, fully train selected architecture with standard recipe and use it for normal task inference.

Sources:
- Sec. 3.4 and experimental protocol sections.
- Inference from source (deployment details are benchmark-specific).

## Complexity and Efficiency
- Time complexity: Dominated by repeated surrogate updates + occasional true training evaluations + evolution offspring scoring.
- Space complexity: Depends on architecture pool size, metric cache, and surrogate parameters.
- Runtime characteristics: Uses many cheap metric/surrogate evaluations with few expensive true-training updates.
- Scaling notes: Evolution module is used for large spaces (e.g., DARTS), while smaller benchmark spaces can skip evolution.

## Implementation Notes
- Metrics used: grad_norm, snip, grasp, fisher, synflow, jacob_cov.
- Metric/value normalization: Eq. (10), weight normalization Eq. (11) in Appendix B.2.
- Surrogate score includes both positive and negative metric effects via split weights (Eq. 5).
- Loss threshold and difference threshold \(T_{th}\) are critical for stability.
- Evolution detail: shortest operation path/minimum operation cost and adaptive exploration weight \(N\).
- Reproducibility caveat: official anonymous code URL in PDF is currently not clonable.

## Comparison to Related Methods
- Compared with HNAS: PO-NAS emphasizes per-architecture metric weighting, not only global adaptation.
- Compared with RoBoT: similar hybrid spirit, but PO-NAS adds architecture-specific weights and dedicated evolution stage.
- Main advantage: Better adaptation to architecture heterogeneity in metric sensitivity.
- Main tradeoff: More moving parts and higher optimization instability risk.

## Evidence and Traceability
- Key figure(s): Fig. 1 (pipeline), Fig. 2 (surrogate design), Fig. 3 (search behavior).
- Key table(s): Table 1 (NAS-Bench-201), Table 2 (ImageNet/DARTS), Table 3 (TransNAS-Bench-101).
- Key equation(s): Eq. (1)-(9) main method, Eq. (10)-(11) normalization.
- Key algorithm(s): Algorithm 1 (main loop), Algorithm 2 (operation path/cost).

## References
- PDF (local): D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf
- Code URL (anonymous): https://anonymous.4open.science/r/PO-NAS-2953
- Local implementation: Not archived (anonymous repository not found on 2026-03-16)
