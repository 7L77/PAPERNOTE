---
title: "NAS-Bench-201"
type: method
source_paper: "NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search"
source_note: "[[NAS-Bench-201]]"
authors: [Xuanyi Dong, Yi Yang]
year: 2020
venue: ICLR
tags: [nas-method, benchmark, reproducibility, cell-based-nas]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-Bench-201

## One-line Summary
> NAS-Bench-201 turns NAS comparison into a controlled benchmark problem by exhaustively evaluating a compact cell search space (`5^6=15625`) under unified protocols and exposing queryable API metrics.

## Source
- Paper: [NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search](https://arxiv.org/abs/2001.00326)
- HTML: https://arxiv.org/html/2001.00326
- Code: https://github.com/D-X-Y/NAS-Bench-201
- Paper note: [[NAS-Bench-201]]

## Applicable Scenarios
- Problem type: Fair and reproducible evaluation of NAS search algorithms.
- Assumptions: Candidate methods can operate on a cell-based discrete search space.
- Data regime: Offline tabular benchmark querying; optional simulated search loops.
- Scale / constraints: 15,625 candidate cells with precomputed training/evaluation traces.
- Why it fits: It decouples search-policy quality from expensive repeated model retraining.

## Not a Good Fit When
- You need direct conclusions on very large modern search spaces without transfer checks.
- Your NAS method fundamentally depends on macro-level search dimensions not represented in this cell space.
- You require end-to-end benchmark generation rather than benchmark querying.

## Inputs, Outputs, and Objective
- Inputs: Cell architecture encoding / architecture string / architecture index; dataset choice and protocol (12-epoch or 200-epoch settings).
- Outputs: Train/validation/test metrics, FLOPs, params, latency, and architecture ranking signals.
- Objective: Provide reproducible, comparable evidence for NAS algorithm behavior.
- Core assumptions: Unified training protocol can act as a stable reference signal for algorithm comparison.

## Method Breakdown

### Stage 1: Define algorithm-agnostic cell search space
- Build a 4-node DAG cell where each of 6 directed edges selects one of 5 operations.
- Enumerate all architecture encodings (`5^6=15625`).
- Source: Sec. 2.1, Fig. 1, Appendix A.

### Stage 2: Exhaustively evaluate all candidates
- Train every architecture on CIFAR-10, CIFAR-100, and ImageNet16-120 with unified setup.
- Record full epoch-wise metrics and computational costs.
- Source: Sec. 2.2-2.4, Table 1-2.

### Stage 3: Expose benchmark through API + diagnostics
- Provide direct query interfaces for architecture metrics and trial details.
- Include diagnostics for convergence dynamics and cost-aware analysis.
- Source: Sec. 2.4, Appendix D, repository `nas_201_api`.

### Stage 4: Benchmark representative NAS algorithms
- Re-implement and evaluate 10 NAS families under shared benchmark constraints.
- Analyze parameter-sharing behavior, BN handling, and search-time speedups.
- Source: Sec. 5, Table 4-5, Fig. 6-8, Table 7.

## Pseudocode

```text
Algorithm: NAS-Bench-201 Construction and Usage
Input: Operation set O (|O|=5), node count V=4, datasets D={CIFAR-10, CIFAR-100, ImageNet16-120}
Output: Queryable benchmark table and API for NAS evaluation

1. Construct dense directed cell graph with V=4 nodes and 6 ordered edges.
   Source: Sec. 2.1, Fig. 1
2. Enumerate all edge-operation assignments over O to get 5^6=15625 candidates.
   Source: Sec. 2.1, Appendix A
3. For each architecture a and each dataset d in D, train with unified protocol (H_main), and optional short-budget protocol (H_short for CIFAR-10).
   Source: Sec. 2.3, Table 1, Appendix A
4. Log epoch-wise train/valid/test metrics plus FLOPs/params/latency.
   Source: Sec. 2.3-2.4, Table 2
5. Package architecture records into API-indexable benchmark files.
   Source: Appendix D, repository API (`NASBench201API`)
6. Evaluate search algorithms by querying benchmark records instead of retraining each selected architecture.
   Source: Sec. 5, Table 4-5
```

## Training Pipeline

1. Define fixed macro skeleton and cell-level search space.
2. Enumerate all architecture encodings.
3. Train each architecture with shared hyperparameters (`H_main`, plus `H_short` option for short-budget CIFAR-10 studies).
4. Store metrics and checkpoints in benchmark files.

Sources:
- Sec. 2.1-2.3
- Table 1-2
- Appendix A / Appendix D

## Inference Pipeline

1. Initialize `NASBench201API` with benchmark file.
2. Query architecture by index or architecture string.
3. Retrieve metrics/costs and rank candidates for a target search algorithm.

Sources:
- Appendix D
- Repository `README.md` and `nas_201_api/api_201.py`

## Complexity and Efficiency
- Time complexity: One-time benchmark creation is very expensive (full training for all 15,625 architectures).
- Space complexity: Large benchmark artifacts and optional per-architecture weight archives.
- Runtime characteristics: Once built, lookup-based evaluation reduces many search/evaluation steps to seconds for non-parameter-sharing methods.
- Scaling notes: Exhaustive evaluation approach becomes impractical for much larger spaces; authors discuss this as a limitation.

## Implementation Notes
- API class: `NASBench201API` in `nas_201_api/api_201.py`.
- Supported benchmark files include `NAS-Bench-201-v1_0-e61699.pth` and `NAS-Bench-201-v1_1-096897.pth`.
- Repository is marked deprecated and points users to NATS-Bench for extended functionality.
- Practical gotcha: Benchmark querying is lightweight, but reproducing full assets requires very large data/model downloads.

## Comparison to Related Methods
- Compared with NAS-Bench-101: NAS-Bench-201 uses edge-based operations and removes edge-count constraints for broader algorithm compatibility.
- Compared with [[Surrogate NAS Benchmark]]: NAS-Bench-201 is an exhaustive tabular benchmark in a compact space, while surrogate benchmarks trade exactness for larger-space scalability.
- Main advantage: Strong reproducibility and fairer apples-to-apples NAS algorithm comparison.
- Main tradeoff: Limited representational scope of the compact search space.

## Evidence and Traceability
- Key figure(s): Fig. 1 (space design), Fig. 2-5 (performance/ranking/correlation), Fig. 6-8 (algorithm behavior).
- Key table(s): Table 1-7.
- Key equation(s): No core optimization equation; main contribution is benchmark construction protocol.
- Key algorithm(s): API-based query and evaluation protocol (Appendix D), benchmarking setup (Sec. 5).

## References
- arXiv: https://arxiv.org/abs/2001.00326
- HTML: https://arxiv.org/html/2001.00326
- Code: https://github.com/D-X-Y/NAS-Bench-201
- Local implementation: D:/PRO/essays/code_depots/NAS-Bench-201 extending the scope of reproducible neural architecture search
