---
title: "NAS-RobBench-201"
type: method
source_paper: "Robust NAS benchmark under adversarial training: assessment, theory, and beyond"
source_note: "[[NAS-RobBench-201]]"
authors: [Yongtao Wu, Fanghui Liu, Carl-Johann Simon-Gabriel, Grigorios G. Chrysos, Volkan Cevher]
year: 2024
venue: ICLR
tags: [nas-method, robust-nas, benchmark, adversarial-training, ntk]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-RobBench-201

## One-line Summary
> NAS-RobBench-201 is a robust-NAS benchmark pipeline that pretrains/evaluates 6466 non-isomorphic NAS-Bench-201 architectures under adversarial training and supports train-free screening through robust NTK analysis.

## Source
- Paper: [Robust NAS benchmark under adversarial training: assessment, theory, and beyond](https://openreview.net/forum?id=cdUpf6t6LZ)
- Project: https://tt2408.github.io/nasrobbench201hp/
- Code: https://github.com/TT2408/nasrobbench201
- Paper note: [[NAS-RobBench-201]]
- Local implementation: `D:/PRO/essays/code_depots/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond`

## Applicable Scenarios
- Problem type: Robust architecture selection/evaluation in NAS-Bench-201-style search space.
- Assumptions: You accept NAS-Bench-201 cell space and adversarial-training protocol used in the benchmark.
- Data regime: Vision classification (CIFAR-10/100, ImageNet-16-120) with adversarial training.
- Scale / constraints: Ideal when you want many architecture evaluations without re-running full adversarial training each time.
- Why it fits: Once benchmark is built, algorithm comparison can be done by query/look-up instead of expensive full retraining.

## Not a Good Fit When
- You need transformer/LLM search spaces rather than NAS-Bench-201.
- You need guarantees under very different threat models not covered by the provided metrics.
- You need low-level deployment constraints (latency/energy) as first-class optimization targets.

## Inputs, Outputs, and Objective
- Inputs: Architecture IDs in NAS-Bench-201 non-isomorphic set, adversarial-training hyperparameters, dataset split.
- Outputs: Clean and robust accuracy tables for each architecture and dataset.
- Objective: Build a reproducible robust NAS lookup benchmark and provide theory for robust search signals.
- Core assumptions: Multi-objective adversarial training objective can be analyzed via NTK-style kernels.

## Method Breakdown

### Stage 1: Enumerate and Train Architectures
- Enumerate 6466 non-isomorphic architectures from NAS-Bench-201 space.
- Adversarially train each architecture with fixed protocol (PGD-based training).
- Repeat across datasets and seeds.
- Source: Sec. 3.1, Fig. 1.

### Stage 2: Evaluate and Build Lookup Table
- Evaluate clean, FGSM, PGD, APGD/AutoAttack metrics.
- Store architecture-level performance for direct querying.
- Source: Sec. 3.1-3.2, Table 1-2.

### Stage 3: Theory and NTK-Based Screening Insight
- Define multi-objective robust-training objective.
- Derive mixed NTK matrices for clean/robust generalization bounds.
- Analyze Spearman correlation between NTK-scores and robust metrics.
- Source: Sec. 4, Eq. (3)-(6), Theorem 1, Corollary 1, Fig. 5.

## Pseudocode
```text
Algorithm: Build-and-Use NAS-RobBench-201
Input: NAS-Bench-201 space S, datasets D, adversarial trainer A_eps, beta, seeds R
Output: Benchmark table B with clean/robust metrics

1. Enumerate non-isomorphic architectures S' (|S'| = 6466) from NAS-Bench-201.
   Source: Sec. 3.1
2. For each architecture a in S', dataset d in D, seed r in R:
   train network under adversarial training objective:
   L = (1-beta)L_clean + beta L_robust.
   Source: Sec. 3.1 and Eq. (3)
3. Evaluate trained models on clean + FGSM/PGD (+ APGD/AutoAttack) metrics.
   Source: Sec. 3.1
4. Store results into lookup benchmark B for robust NAS algorithms.
   Source: Sec. 3.2, Table 2
5. Optionally compute NTK-based scores (clean/robust/twice-perturbed variants)
   to rank architectures in a train-free manner.
   Source: Sec. 4.2-4.3, Eq. (4)-(5), Fig. 5
```

## Training Pipeline
1. Data preprocessing and augmentation per dataset.
2. PGD-based adversarial training per architecture (fixed hyperparameters).
3. Multi-seed repeated runs.
4. Aggregate metrics across attacks and datasets.

Sources:
- Sec. 3.1
- Table 1-2

## Inference Pipeline
1. Select architecture candidates.
2. Query benchmark table for clean/robust metrics.
3. Rank/select architecture according to robust objective.
4. Optionally retrain selected top architectures for final confirmation.

Sources:
- Sec. 3.2
- Table 2 and Appendix Table 7

## Complexity and Efficiency
- Benchmark build cost: around 107k GPU hours (one-time heavy cost).
- Query-time cost after build: near O(1) lookup per architecture-metric pair.
- Runtime characteristics: expensive offline construction, cheap online NAS evaluation.
- Scaling notes: attack strength and dataset count both increase preprocessing/training burden.

## Implementation Notes
- Search space operators: {3x3 conv, 1x1 conv, zeroize, skip, 1x1 avg pool}.
- Adversarial training setup in paper: PGD-7, eps=8/255, step=2/255, 50 epochs, batch 256.
- Robust metrics include FGSM/PGD with eps in {3/255, 8/255}, plus AutoAttack.
- NTK analysis uses minimum-eigenvalue-related score approximations for efficient ranking.

## Comparison to Related Methods
- Compared with [[NAS-Bench-201]]:
  NAS-RobBench-201 adds adversarial-training-based robust metrics.
- Compared with [[RobustBench]]:
  NAS-RobBench-201 targets architecture-search lookup in a fixed NAS space, not model zoo leaderboard only.
- Main advantage: robust-NAS-friendly tabular benchmark + theory bridge.
- Main tradeoff: tied to a specific search space/protocol and high upfront construction cost.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- Key table(s): Table 1, Table 2, Table 6, Table 7 (appendix)
- Key equation(s): Eq. (3), Eq. (4), Eq. (5), Eq. (6)
- Key algorithm(s): Algorithm 1

## References
- OpenReview: https://openreview.net/forum?id=cdUpf6t6LZ
- Project: https://tt2408.github.io/nasrobbench201hp/
- Code: https://github.com/TT2408/nasrobbench201
- Local implementation: D:/PRO/essays/code_depots/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond

