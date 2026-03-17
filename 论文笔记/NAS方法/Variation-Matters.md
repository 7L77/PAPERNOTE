---
title: "Variation-Matters"
type: method
source_paper: "Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation"
source_note: "[[Variation-Matters]]"
authors: [Pavel Rumiantsev, Mark Coates]
year: 2025
venue: arXiv
tags: [nas-method, zero-shot-nas, training-free-nas, statistical-testing]
created: 2026-03-16
updated: 2026-03-16
---

# Variation-Matters

## One-line Summary
> Treat repeated zero-shot ranking outputs as samples from a random variable, and select architectures via stochastic-statistical comparison (Mann-Whitney based) rather than plain mean aggregation.

## Source
- Paper: [Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation](https://arxiv.org/abs/2502.19657)
- HTML: https://arxiv.org/html/2502.19657v1
- Code: Not found in paper/arXiv metadata (as checked on 2026-03-16)
- Paper note: [[Variation-Matters]]

## Applicable Scenarios
- Problem type: Zero-shot NAS candidate ranking under noisy proxy evaluations.
- Assumptions: Each architecture can be evaluated multiple times (`V` repeats), and higher proxy value tends to indicate better final performance.
- Data regime: Offline benchmark search (NAS-Bench family, TransNAS-Bench).
- Scale / constraints: When full training is too expensive but repeated cheap proxy evaluation is feasible.
- Why it fits: It uses ranking-score distributions directly, preserving uncertainty information ignored by averaging.

## Not a Good Fit When
- Ranking metrics are almost deterministic (very low variation), where averaging is already sufficient.
- Statistical test assumptions or sample size are too weak to provide meaningful decisions.
- You need strict global-optimality guarantees beyond heuristic search.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture set, ranking function `r`, batch size `B`, repeats `V`, significance threshold `alpha`.
- Outputs: Selected architecture (or top-k) from random/evolutionary search.
- Objective: Improve selected architecture quality and search stability under ranking noise.
- Core assumptions: Repeated evaluations approximate a meaningful score distribution per architecture.

## Method Breakdown

### Stage 1: Measure ranking variation
- Compute per-architecture sample set `M_i={r(arch_i, d_v)}_{v=1}^V`.
- Aggregate variation via average coefficient of variation across the search space.
- Source: Sec. 4.1, Eq. (1).

### Stage 2: Statistical comparator
- For two architectures, compare score samples with one-sided Mann-Whitney U-test.
- Accept superiority only when p-value is below threshold.
- Source: Sec. 4.2, lines around Algorithm 1.

### Stage 3: Integrate into search
- Random search: replace mean-based max with `Stat-MAX`.
- Evolutionary search (REA/FreeREA/Greedy): use statistical ordering for tournament and final selection.
- Source: Sec. 4.2, Sec. 5.2, Sec. 5.3, Appendix B.

## Pseudocode
```text
Algorithm: Variation-Matters Comparator-in-Search
Input: ranking function r, candidate set A, repeat count V, threshold alpha
Output: selected architecture a*

1. For each queried architecture a, collect V scores:
   S(a) = {r(a, d_v)}_{v=1}^V.
   Source: Sec. 4.1 / Sec. 4.2

2. Define StatBetter(a, b):
   run one-sided Mann-Whitney U-test on S(a) and S(b).
   return True if p < alpha and a is stochastically greater.
   Source: Sec. 4.2 / Algorithm 1

3. Stat-MAX over a candidate list:
   keep current best m; if StatBetter(x, m), set m <- x.
   Source: Algorithm 1

4. Plug Stat-MAX / Stat-TOPK into search:
   - random search final choice
   - REA/FreeREA parent and final selection.
   Source: Sec. 4.2 / Appendix B

5. Cache architecture score samples S(a) once encountered.
   Source: Sec. 5.3 / Appendix F
```

## Training Pipeline
1. Build benchmark interface to sample architectures and query proxy scores.
2. For each architecture evaluation, run repeated score computation (`V=10` in paper default).
3. Use statistical comparator in place of mean comparator inside search loop.
4. Track final selected architecture accuracy from benchmark ground truth.

Sources:
- Sec. 5.2, Sec. 5.3
- Appendix B (search pseudocode)

## Inference Pipeline
1. Given a fixed search space and budget, run search using statistical comparator.
2. Return top architecture(s) selected by statistical dominance test.
3. Optionally tune `alpha` in range around `0.025~0.075`.

Sources:
- Sec. 4.2
- Appendix E (threshold ablation)

## Complexity and Efficiency
- Time complexity: Not explicitly provided; comparator cost increases with repeated samples and pairwise tests.
- Space complexity: Extra memory to cache score samples per architecture.
- Runtime characteristics: Slight additional testing overhead; often outweighed by quality gains.
- Scaling notes: Caching is critical in evolutionary search for both stability and quality.

## Implementation Notes
- Must preserve per-architecture repeated score samples instead of collapsing to mean too early.
- Tie handling is effectively random when no significant dominance is detected.
- Statistical threshold `alpha` is a sensitive hyperparameter.
- Data-agnostic proxies (e.g., SynFlow/LogSynFlow) may not always benefit.
- No official repository was linked by the authors in the paper/arXiv page.

## Comparison to Related Methods
- Compared with mean-aggregation search: keeps distributional information and gives more robust comparisons.
- Compared with naive CV-augmented scoring (`mean + CV`): statistical comparison is more consistent across spaces.
- Main advantage: Better average selected accuracy with minimal conceptual changes.
- Main tradeoff: More bookkeeping/testing complexity and threshold tuning.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 3, Fig. 4, Fig. 5.
- Key table(s): Table 1, Table 2, Table 3, Table 7.
- Key equation(s): Eq. (1), Eq. (2) (appendix baseline).
- Key algorithm(s): Algorithm 1, Algorithm 2/3/4 (appendix integration).

## References
- arXiv: https://arxiv.org/abs/2502.19657
- HTML: https://arxiv.org/html/2502.19657v1
- Code: Not found
- Local implementation: Not archived

