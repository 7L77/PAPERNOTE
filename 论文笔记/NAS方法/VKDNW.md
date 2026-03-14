---
title: "VKDNW"
type: method
source_paper: "Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights"
source_note: "[[VKDNW]]"
authors: [Ondrej Tybl, Lukas Neumann]
year: 2025
venue: arXiv
tags: [nas-method, training-free-nas, fisher-information, ranking-proxy]
created: 2026-03-14
updated: 2026-03-14
---

# VKDNW

## One-line Summary

> VKDNW builds a zero-shot NAS ranking signal from the entropy of empirical FIM eigenvalues, then combines it with a size proxy and nDCG-oriented evaluation to better identify top architectures.

## Source

- Paper: [Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights](https://arxiv.org/abs/2502.04975)
- HTML: https://arxiv.org/html/2502.04975v1
- Code: https://github.com/ondratybl/VKDNW
- Paper note: [[VKDNW]]

## Applicable Scenarios

- Problem type: Training-free neural architecture ranking for image classification.
- Assumptions: Architecture quality can be inferred from initialization-time weight-estimation geometry.
- Data regime: Label-free scoring can use random input noise; optional supervised labels for some baseline proxies.
- Scale / constraints: Useful when full training of each candidate is infeasible and ranking quality at top-P matters.
- Why it fits: It separates structure-feasibility information (VKDNW) from capacity proxy (`N_layers`) and targets search-relevant ranking quality.

## Not a Good Fit When

- You need absolute final accuracy prediction rather than ranking quality.
- Search spaces have architectures where sampled-layer FIM is not representative.
- You cannot afford repeated gradient/Jacobian computations over many candidates.

## Inputs, Outputs, and Objective

- Inputs: Architecture `f`, initialized weights `theta_init`, random mini-batch `x`, optional auxiliary zero-cost features for aggregation.
- Outputs: `VKDNW(f)`, `VKDNWsingle(f)`, and optionally aggregated rank `VKDNWagg`.
- Objective: Rank candidate architectures so that high-accuracy models appear early in the list.
- Core assumptions: Empirical FIM spectrum at initialization correlates with trainability/quality ordering.

## Method Breakdown

### Stage 1: Empirical FIM Construction

- Build empirical FIM from model-predicted class probabilities, not true labels.
- Use numerically stable decomposition and low-dimensional parameter sampling.
- Source: Sec. II-B, Eq. (8), Eq. (9), Eq. (10).

### Stage 2: VKDNW Score from Spectrum Entropy

- Extract decile eigenvalue representatives, normalize them, and compute entropy.
- Exclude unstable extreme eigenvalues for robustness.
- Source: Sec. II-C, Eq. (11), footnote near Eq. (11).

### Stage 3: Size-aware Single Ranking

- Combine architecture-size proxy (`N_layers`) with VKDNW entropy score.
- This effectively groups by size first and sorts by VKDNW within groups.
- Source: Sec. III(a), Eq. (12).

### Stage 4: Optional Aggregated Ranking

- Aggregate V/J/E/T/F rankings with log-product non-linear rule.
- Optional model-driven aggregation uses RandomForest over feature sets.
- Source: Sec. V-A, Eq. (15), Table I, Table III.

### Stage 5: NAS-oriented Evaluation

- Evaluate ranking quality with KT, SPR, and especially nDCG@P for top architectures.
- Source: Sec. III, Eq. (13), Eq. (14), Fig. 2.

## Pseudocode

```text
Algorithm: VKDNW-based Training-free Ranking
Input: Candidate architecture set F, random batch size B, top cutoff P
Output: Ranked architectures (single or aggregated)

1. For each architecture f in F, initialize weights theta_init.
   Source: Sec. II-C
2. Compute empirical FIM approximation with stable factorization:
   F_hat(theta) = (1/N) * sum_n A_n^T A_n, using sampled parameters.
   Source: Sec. II-B, Eq. (8)-(10)
3. Compute VKDNW(f) as entropy over normalized decile eigenvalues.
   Source: Sec. II-C, Eq. (11)
4. Compute VKDNWsingle(f) = N_layers(f) + VKDNW(f).
   Source: Sec. III(a), Eq. (12)
5. Optionally aggregate with Jacov/Expressivity/Trainability/FLOPs:
   rank_agg(f) = log(prod_j rank_j(f)).
   Source: Sec. V-A, Eq. (15)
6. Use ranking for search and evaluate with KT/SPR/nDCG@P.
   Source: Sec. III, Eq. (13)-(14)
```

## Training Pipeline

1. Generate random inputs (or task inputs for baseline comparisons).
2. Compute per-architecture proxy scores at initialization.
3. Build ranking (`VKDNWsingle` or `VKDNWagg`).
4. In search loops, keep top candidates and mutate/evolve.
5. Fully train only shortlisted final architectures.

Sources:

- Sec. V-A, Sec. V-B, Table II, supplementary Sec. VIII-IX.

## Inference Pipeline

1. Given a new candidate architecture, run initialization.
2. Compute empirical FIM-based VKDNW score.
3. Convert score to ranking among current candidate pool.
4. Select top architectures for downstream full training/evaluation.

Sources:

- Sec. II-B, Sec. II-C, Sec. III(a), Sec. V.

## Complexity and Efficiency

- Time complexity: Not provided as closed-form in the paper.
- Space complexity: Not provided as closed-form in the paper.
- Runtime characteristics: Proxy-based search is reported as ZS 0.4 GPU days in MobileNetV2 setting; final full training still dominates cost (7 days on 8x A100 for selected model).
- Scaling notes: Parameter sampling (e.g., first 128 layers, few weights per layer) is used to keep FIM computations tractable.

## Implementation Notes

- FIM approximation uses stable decomposition and singular-value-friendly computation.
- Default practical choice in ablations: batch size 64 and random input works similarly to real input.
- Parameter sampling: one weight per layer across first 128 layers is a robust tradeoff.
- Aggregation components: V (VKDNWsingle), J (Jacov), E (Expressivity), T (Trainability), F (FLOPs).
- Model-driven aggregation uses RandomForest trained on 1024 architectures.
- Code status in this workspace: official repo identified but local clone incomplete due GitHub connectivity timeout on 2026-03-14.

## Comparison to Related Methods

- Compared with [[Zero-Cost Proxy]] baselines: adds a Fisher-spectrum-derived signal with explicit statistical grounding.
- Compared with [[AZ-NAS]]: stronger top-ranking behavior in nDCG while keeping competitive KT/SPR.
- Main advantage: better top-architecture discrimination and orthogonality to size proxies.
- Main tradeoff: still requires gradient-based computations and, for best performance, auxiliary aggregation components.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4.
- Key table(s): Table I, Table II, Table III, Table V, Table VII, Table VIII.
- Key equation(s): Eq. (8)-(12), Eq. (14), Eq. (15).
- Key algorithm(s): Evolutionary-search replacement described in Sec. V-B and supplementary Sec. VIII.

## References

- arXiv: https://arxiv.org/abs/2502.04975
- HTML: https://arxiv.org/html/2502.04975v1
- Code: https://github.com/ondratybl/VKDNW
- Local implementation: Not archived (GitHub connectivity timeout on 2026-03-14)
