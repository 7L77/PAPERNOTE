---
title: "REP"
type: method
source_paper: "REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search"
source_note: "[[REP]]"
authors: [Yuqi Feng, Yanan Sun, Gary G. Yen, Kay Chen Tan]
year: 2025
venue: IEEE TKDE
tags: [nas-method, robust-nas, differentiable-nas, plugin, adversarial-robustness]
created: 2026-03-14
updated: 2026-03-14
---

# REP

## One-line Summary
> REP is a plugin for differentiable NAS that first samples robust search primitives from architecture-robustness trajectories, then biases architecture optimization toward those primitives via a distance regularizer.

## Source
- Paper: [REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search](https://doi.org/10.1109/TKDE.2025.3543503)
- HTML: Not reported in the paper
- Code: https://github.com/fyqsama/REP
- Paper note: [[REP]]

## Applicable Scenarios
- Problem type: Robust architecture search under adversarial attacks in differentiable NAS.
- Assumptions: Architecture can be represented as search primitives `(edge, op)`; robust performance under chosen attacks is measurable during search.
- Data regime: CNN image classification and GNN node classification.
- Scale / constraints: Suitable when full per-architecture training is too expensive and supernet-based search is used.
- Why it fits: REP only adds sampling + regularization around existing differentiable NAS pipelines.

## Not a Good Fit When
- No reliable adversarial robustness evaluator is available during search.
- Search space is not primitive-based or cannot map cleanly to `(edge, op)` indicators.
- You need architecture diversity beyond cell-based settings as a first priority.

## Inputs, Outputs, and Objective
- Inputs: Search space `S`, search policy `P`, architecture sequence `A`, robustness scores `R`, trade-off coefficient `lambda`.
- Outputs: Final architecture with improved robustness and competitive natural accuracy.
- Objective: Minimize validation loss while shrinking distance to robust-primitive indicator matrix.
- Core assumptions: Primitive differences between adjacent architectures explain robustness differences better than non-adjacent comparisons.

## Method Breakdown

### Stage 1: Architecture Pooling and Robustness Evaluation
- Run baseline differentiable NAS for multiple epochs, record candidate architectures.
- Evaluate each unique architecture under adversarial attacks to build `(A, R)`.
- Source: Sec. III-B (lines 3-13 in Algorithm 1), Sec. IV-C (attack settings)

### Stage 2: Robust Primitive Sampling
- Compare adjacent architecture pairs.
- If robustness improves (`Ri < Ri+1`), add primitives in `Ai+1 \ Ai` to `B1`; otherwise add `Ai \ Ai+1` to `B2`.
- Keep intersection `B = B1 ∩ B2` as robust primitives.
- Source: Sec. III-C, Algorithm 2, Fig. 2, Fig. 3

### Stage 3: Probability Enhancement Search
- Build binary indicator matrix `alpha_R` from sampled robust primitives.
- Add distance loss `||alpha - alpha_R||^2` to differentiable NAS objective.
- Optimize architecture and network parameters in the same bi-level framework as baseline NAS.
- Source: Sec. III-D, Eq. (3)-(6)

## Pseudocode
```text
Algorithm: REP
Input: Search space S, differentiable NAS policy P, epochs N, attack evaluator Attack(.), trade-off lambda
Output: Robust architecture A*

1. Initialize architecture list A = [] and robustness list R = [].
   Source: Sec. III-B, Algorithm 1
2. For epoch i = 1..N:
   2.1 Run one epoch of baseline differentiable NAS and get architecture Ai.
       Source: Sec. III-B, Algorithm 1
   2.2 If Ai already appears in A, reuse previous robustness score.
       Source: Sec. III-B (architecture dedup note)
   2.3 Else evaluate robustness Ri = Attack(Ai) and append (Ai, Ri) to (A, R).
       Source: Sec. III-B (lines 7-11)
3. Build B1 and B2 by scanning adjacent pairs (Ai, Ai+1):
   3.1 If Ri < Ri+1, add Ai+1 \ Ai to B1.
       Source: Sec. III-C, Algorithm 2
   3.2 Else add Ai \ Ai+1 to B2.
       Source: Sec. III-C, Algorithm 2
4. Set robust primitive set B = B1 ∩ B2.
   Source: Sec. III-C, Algorithm 2
5. Construct indicator alpha_R from B (1 for robust primitive positions, else 0).
   Source: Eq. (3)
6. Optimize:
      min_alpha L_val(w*(alpha), alpha) + lambda * ||alpha - alpha_R||^2
      s.t. w*(alpha) = argmin_w L_train(w, alpha)
   Source: Eq. (4)-(6)
7. Derive final discrete architecture A* from optimized alpha.
   Source: Eq. (2), Sec. III-D
```

## Training Pipeline
1. Search phase with supernet optimization (same as baseline differentiable NAS).
2. During search, periodically evaluate robust accuracy of unique candidate architectures.
3. Sample robust primitives from adjacent architecture-robustness trajectory.
4. Re-run/search with probability-enhancement objective including distance regularization.
5. Retrain final architecture with standard/adversarial training for final reporting.

Sources:
- Sec. III-B, III-C, III-D
- Sec. IV-C

## Inference Pipeline
1. Freeze searched architecture.
2. Load trained checkpoint.
3. Evaluate on clean and adversarial examples (FGSM/PGD/APGD/C&W for CNN; graph attacks for GNN).

Sources:
- Sec. IV-C, Sec. V-A, V-B
- Source: Inference from source

## Complexity and Efficiency
- Time complexity: Not reported in closed form.
- Space complexity: Not reported in closed form.
- Runtime characteristics:
  - CNN search cost around `0.7 GPU days`.
  - Decomposed cost: original search `~0.5`, robust evaluation `~0.18`, probability-enhanced search `~0.07` GPU days.
  - GNN search cost around `0.0015 GPU days`.
- Scaling notes: Additional cost comes mainly from adversarial robustness evaluation for sampled architectures.

## Implementation Notes
- Local code path: `D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search`.
- `CNN/darts/train_search.py` records candidate genotypes and evaluates FGSM/PGD robustness during search.
- `CNN/darts/sample.py` concretely constructs `B1/B2` and intersection primitives from recorded architecture trajectory.
- `CNN/darts/architect.py` applies the distance regularizer with hard-coded robust-primitive indicator matrices.
- `GNN/architect.py` mirrors the idea with `NA_primitives`-guided distance regularization.
- Practical gotcha: current code stores sampled robust primitive templates explicitly; changing attack setup typically requires re-sampling/updating those templates.

## Comparison to Related Methods
- Compared with [[AdvRush]]-style regularization: REP gives explicit primitive-level interpretability.
- Compared with plain [[DARTS]]/[[PDARTS]]/[[PCDARTS]]: REP improves robustness while keeping the same differentiable search backbone.
- Main advantage: Plugin-style integration plus better process/result interpretability.
- Main tradeoff: Needs adversarial evaluation during search and may depend on chosen attack type.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6, Fig. 7
- Key table(s): Table I, II, III, IV, V, VI, VII, VIII, IX, X
- Key equation(s): Eq. (3), Eq. (4), Eq. (5), Eq. (6), plus DARTS Eq. (2)
- Key algorithm(s): Algorithm 1, Algorithm 2

## References
- DOI: https://doi.org/10.1109/TKDE.2025.3543503
- Code: https://github.com/fyqsama/REP
- Local implementation: D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search
