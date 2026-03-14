---
title: "AZ-NAS"
type: method
source_paper: "AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search"
source_note: "[[AZ-NAS]]"
authors: [Junghyup Lee, Bumsub Ham]
year: 2024
venue: CVPR
tags: [nas-method, nas, training-free, zero-cost-proxy]
created: 2026-03-14
updated: 2026-03-14
---

# AZ-NAS

## One-line Summary
> AZ-NAS uses four complementary zero-cost proxies and a non-linear rank aggregation rule to make training-free NAS rankings more aligned with final architecture performance.

## Source
- Paper: [AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search](https://arxiv.org/abs/2403.19232)
- HTML: https://arxiv.org/html/2403.19232
- Code: https://github.com/cvlab-yonsei/AZ-NAS
- Paper note: [[AZ-NAS]]

## Applicable Scenarios
- Problem type: Training-free architecture ranking and evolutionary NAS under compute budgets.
- Assumptions: Candidate architectures can expose block features/gradients at initialization.
- Data regime: Primarily image-classification NAS benchmarks/search spaces.
- Scale / constraints: Large candidate pools where full training for each candidate is infeasible.
- Why it fits: The proxy bundle captures diverse signals (feature geometry, depth progression, gradient stability, cost).

## Not a Good Fit When
- You need strict hardware latency optimization rather than FLOPs-guided proxying.
- Architectures do not support meaningful block-level feature extraction.
- Domain shift is large and proxy-final-performance correlation is unknown.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture, random Gaussian batch, compute budget, top-k mutation policy.
- Outputs: Aggregated AZ score per candidate and the best architecture after search.
- Objective: Maximize ranking consistency with true final accuracy while keeping search cheap.
- Core assumptions: Better multi-proxy rank consistency leads to better selected architectures.

## Method Breakdown

### Stage 1: Proxy Computation (`sE, sP, sT, sC`)
- Compute expressivity from entropy of normalized PCA eigenvalues across primary blocks.
- Compute progressivity from minimum layer-to-layer expressivity gain.
- Compute trainability from a Jacobian spectral-norm surrogate using Rademacher vectors.
- Compute complexity from FLOPs.
- Source: Sec. 3.1, Eq. (1)-(11)

### Stage 2: Non-linear Rank Aggregation
- For each proxy, rank all candidates.
- Aggregate with `sum(log(rank/m))` to penalize weak dimensions.
- Source: Sec. 3.2, Eq. (12)

### Stage 3: Evolutionary Search Loop
- Maintain history of candidates and proxy scores.
- Re-rank with AZ score, mutate top-k candidates under budget constraints.
- Return highest-score architecture.
- Source: Algorithm 1, Sec. 4.1

## Pseudocode
```text
Algorithm: AZ-NAS
Input: Search space Z, iterations T, budget B, top-k size k
Output: Best architecture F*

1. Initialize candidate F1 and empty history {F, SE, SP, ST, SC}.
   Source: Algorithm 1 (line 1-2)
2. For i = 1..T:
   2.1 Compute sE, sP, sT, sC for Fi.
       Source: Sec. 3.1, Eq. (1)-(11)
   2.2 Append Fi and proxy scores to history.
       Source: Algorithm 1 (line 4-5)
   2.3 Compute AZ scores with non-linear rank aggregation.
       Source: Sec. 3.2, Eq. (12), Algorithm 1 (line 6)
   2.4 Mutate one of top-k candidates to get Fi+1 under budget B.
       Source: Algorithm 1 (line 7)
3. Return highest-score architecture in history.
   Source: Algorithm 1 (line 9)
```

## Training Pipeline
1. Search phase: compute proxies on randomly initialized models with random Gaussian input batch.
2. Rank candidates by AZ score and run evolutionary updates.
3. Select best architecture under FLOPs/params constraints.
4. Retrain selected architecture with standard training recipe for final accuracy.

Sources:
- Sec. 4.1, Algorithm 1, Table 2/3

## Inference Pipeline
1. Freeze selected architecture from search.
2. Train/fine-tune according to target benchmark protocol.
3. Run standard forward inference for evaluation.

Sources:
- Sec. 4.2, Table 2, Table 3
- Inference from source

## Complexity and Efficiency
- Time complexity: Not given in closed form.
- Space complexity: Not given in closed form.
- Runtime characteristics: On NAS-Bench-201, reported around `42.7 ms/arch`, much lower than heavier baselines like TE-NAS.
- Scaling notes: More proxies + non-linear aggregation improve rank consistency; adding proxies increases runtime moderately.

## Implementation Notes
- Core MBV2 proxy implementation: `ImageNet_MBV2/ZeroShotProxy/compute_az_nas_score.py`.
- MBV2 search loop: `ImageNet_MBV2/evolution_search_az.py`.
- AutoFormer proxy implementation: `ImageNet_AutoFormer/lib/training_free/indicators/az_nas.py`.
- Important practical detail: AutoFormer branch omits progressivity (`sP`), matching the paper footnote for ViTs.
- Aggregation implementation in code uses `np.log(stats.rankdata(score)/l)` summed across proxies, aligned with Eq. (12).
- Initialization detail in MBV2 proxy code uses Kaiming fan-in init before scoring.

## Comparison to Related Methods
- Compared with TE-NAS: AZ-NAS keeps lower runtime while improving ranking consistency.
- Compared with ZiCo/SynFlow: AZ-NAS combines broader proxy views and stronger aggregation.
- Main advantage: Better performance-cost tradeoff with clear proxy interpretability.
- Main tradeoff: Still benchmark/search-space dependent and not a guarantee of cross-domain ranking quality.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 3
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5
- Key equation(s): Eq. (1)-(12)
- Key algorithm(s): Algorithm 1

## References
- arXiv: https://arxiv.org/abs/2403.19232
- HTML: https://arxiv.org/html/2403.19232
- Code: https://github.com/cvlab-yonsei/AZ-NAS
- Local implementation: D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search

