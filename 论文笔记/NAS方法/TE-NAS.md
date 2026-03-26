---
title: "TE-NAS"
type: method
source_paper: "Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective"
source_note: "[[TE-NAS]]"
authors: [Wuyang Chen, Xinyu Gong, Zhangyang Wang]
year: 2021
venue: ICLR
tags: [nas-method, nas, training-free, ntk, linear-regions]
created: 2026-03-26
updated: 2026-03-26
---

# TE-NAS

## One-line Summary
> TE-NAS prunes supernet operators by summing two rank signals derived from operator-removal effects on NTK conditioning (trainability) and linear-region count (expressivity), enabling fast training-free NAS.

## Source
- Paper: [Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective](https://arxiv.org/abs/2102.11535)
- HTML: https://arxiv.org/html/2102.11535
- Code: https://github.com/VITA-Group/TENAS
- Paper note: [[TE-NAS]]

## Applicable Scenarios
- Problem type: training-free architecture search / ranking in cell-based search spaces.
- Assumptions: initialization-time proxies correlate with downstream architecture quality.
- Data regime: image classification search spaces (NAS-Bench-201, DARTS).
- Scale / constraints: low search budget, but enough memory/compute to evaluate NTK and region statistics repeatedly.
- Why it fits: separates trainability and expressivity signals and combines them in a stable rank-based criterion.

## Not a Good Fit When
- The target domain is far from image-classification cell spaces and proxy correlation is unvalidated.
- Candidate architectures do not use ReLU-like activation patterns where linear-region counting is meaningful.
- Extremely large models make repeated NTK-region evaluation too expensive.

## Inputs, Outputs, and Objective
- Inputs: search space with edges and operator candidates, data loader, initialization strategy, repeat count.
- Outputs: pruned single-path architecture (or DARTS-style final sparse cell).
- Objective: maximize final architecture quality while minimizing search cost, via proxy-driven pruning.
- Core assumptions: low `\kappa_N` and high `\hat{R}_N` jointly indicate stronger architectures.

## Method Breakdown

### Stage 1: Build and initialize supernet
- Initialize full supernet with all operators active.
- Re-initialize network weights with Kaiming rules before each proxy estimate.
- Source: Sec. 3.2, Algorithm 1; Appendix A.

### Stage 2: Score each removable operator by proxy deltas
- For each active operator on each edge, create a temporary pruned variant.
- Compute relative NTK-condition change and linear-region change versus current supernet.
- Repeat estimates multiple times and average.
- Source: Algorithm 1; code in `prune_tenas.py` (`prune_func_rank`) and `lib/procedures/ntk.py`, `lib/procedures/linear_region_counter.py`.

### Stage 3: Rank-sum importance and edge-wise pruning
- Rank candidates by NTK criterion and by region criterion separately.
- Compute `s(o_j)=s_\kappa(o_j)+s_R(o_j)`.
- For each edge, prune the least-important operator(s), then iterate.
- Source: Algorithm 1, Sec. 3.2.

## Pseudocode
```text
Algorithm: TE-NAS
Input: Supernet N0 with E edges and |O| operators per edge, repeat count r
Output: Final pruned architecture N*

1. Initialize full supernet N <- N0.
   Source: Algorithm 1 (line 1)
2. While N is not single-path:
   Source: Algorithm 1 (line 2)
3.   For each active operator oj in N:
     3.1 Create N\oj by masking oj.
         Source: Algorithm 1 (line 3-5)
     3.2 Estimate NTK-change score (average across repeats).
         Source: Algorithm 1 (line 4), Sec. 3.1.1
     3.3 Estimate linear-region-change score (average across repeats).
         Source: Algorithm 1 (line 5), Sec. 3.1.2
4.   Convert both score lists to ranks: s_kappa(oj), s_R(oj).
     Source: Algorithm 1 (line 6-7)
5.   Compute combined importance s(oj)=s_kappa(oj)+s_R(oj).
     Source: Algorithm 1 (line 8)
6.   For each edge, prune operator(s) with lowest importance.
     Source: Algorithm 1 (line 10-12)
7. Return final pruned architecture N*.
   Source: Algorithm 1 (line 14)
```

## Training Pipeline
1. Search phase does not train candidate architectures to convergence.
2. For each pruning decision, evaluate initialization-based proxies (`\kappa_N`, `\hat{R}_N`) with repeated random initialization.
3. Iteratively prune until final architecture form is reached.
4. Retrain searched architecture with standard training recipe for benchmark reporting.

Sources:
- Sec. 3, Sec. 4, Appendix A

## Inference Pipeline
1. Use final searched architecture topology.
2. Perform standard forward inference after retraining.
3. Report test error/top-1/top-5 according to benchmark protocol.

Sources:
- Sec. 4.2, Sec. 4.3
- Source: Inference from source

## Complexity and Efficiency
- Time complexity: not given as a closed form in paper.
- Space complexity: not given as a closed form in paper.
- Runtime characteristics: paper reports ~0.5 GPU hours on NAS-Bench-201 and ~4 GPU hours on DARTS-ImageNet search.
- Scaling notes: each round evaluates many candidate removals; rank-pruning reduces search breadth compared with sampling many complete architectures.

## Implementation Notes
- Search launcher: `prune_launch.py` (dataset/space specific defaults).
- Main loop: `prune_tenas.py::main`.
- NTK condition number from eigenvalue ratio in `lib/procedures/ntk.py`.
- Linear-region estimator through ReLU hooks in `lib/procedures/linear_region_counter.py`.
- Code-level detail: proxy scores are based on *relative deltas after removal* and then rank-summed, which is a practical realization of the paper's ranking idea.
- Important hyperparameters in code: `repeat`, `prune_number`, `batch_size`, `precision`, init mode.

## Comparison to Related Methods
- Compared with NAS w.o. Training (Mellor et al., 2020): TE-NAS extends beyond Jacobian-only signal and improves robustness of ranking via dual-indicator tradeoff.
- Compared with [[Differentiable Architecture Search]] family: much lower search-time training cost, but may trade off absolute best performance in some setups.
- Main advantage: training-free, interpretable, and fast.
- Main tradeoff: proxy validity is search-space dependent.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 3, Fig. 4, Fig. 5, Fig. 8, Fig. 9, Fig. 10
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5)
- Key algorithm(s): Algorithm 1

## References
- arXiv: https://arxiv.org/abs/2102.11535
- HTML: https://arxiv.org/html/2102.11535
- Code: https://github.com/VITA-Group/TENAS
- Local implementation: D:/PRO/essays/code_depots/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective
