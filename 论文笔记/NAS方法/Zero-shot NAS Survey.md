---
title: "Zero-shot NAS Survey"
type: method
source_paper: "Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities"
source_note: "[[Zero-shot NAS Survey]]"
authors: [Guihong Li, Duc Hoang, Kartikeya Bhardwaj, Ming Lin, Zhangyang Wang, Radu Marculescu]
year: 2024
venue: IEEE TPAMI
tags: [nas-method, survey, zero-shot-nas, hardware-aware-nas]
created: 2026-03-20
updated: 2026-03-20
---

# Zero-shot NAS Survey

## One-line Summary

> This paper is a survey rather than a new search algorithm: it organizes zero-shot NAS around proxy design, benchmark choice, hardware-aware evaluation, and failure-mode analysis, then shows that many proxies still do not consistently beat `#Params/#FLOPs` in realistic settings.

## Source

- Paper: [Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities](https://arxiv.org/abs/2307.01998)
- HTML: https://arxiv.org/html/2307.01998v3
- Code: https://github.com/SLDGroup/survey-zero-shot-nas
- Paper note: [[Zero-shot NAS Survey]]

## Applicable Scenarios

- Problem type: Choosing, comparing, or designing zero-shot proxies for NAS under accuracy-only or hardware-aware objectives.
- Assumptions: Candidate architectures can be scored at initialization, benchmark APIs are available, and hardware metrics can be queried or predicted.
- Data regime: Benchmark-driven, supervised CV tasks, plus hardware measurements/predictors.
- Scale / constraints: Useful when full candidate training is too expensive and you need a first-pass ranking or pruning signal.
- Why it fits: The paper provides a practical evaluation framework for deciding when a proxy is worth using and when naive baselines are already hard to beat.

## Not a Good Fit When

- You need a single end-to-end search algorithm that directly outputs SOTA architectures by itself.
- You need a post-2024 survey of newer proxies and LLM-based NAS variants.
- Your search space is far outside the benchmark families studied here and you cannot validate proxy behavior locally.

## Inputs, Outputs, and Objective

- Inputs: Candidate architectures, a chosen proxy family, NAS benchmarks, task datasets, and optional hardware constraints/latency models.
- Outputs: Proxy scores, rank-correlation analyses, best proxy-selected architectures, and design guidelines for future proxy construction.
- Objective: Understand which zero-shot proxies correlate with final accuracy and when they remain useful under scale and hardware constraints.
- Core assumptions: Initialization-stage statistics contain enough signal to rank candidate networks, at least approximately.

## Method Breakdown

### Stage 1: Define What a Good Proxy Should Measure

- The paper argues that a good proxy should capture expressive capacity, generalization capacity, and trainability rather than only one axis.
- Source: Sec. 2.1, Table 2

### Stage 2: Categorize Existing Proxies

- Group proxies into gradient-based and gradient-free families, then connect each one to its underlying theory.
- Source: Sec. 2.2, Sec. 2.3, Table 2

### Stage 3: Choose Benchmarks and Hardware Models

- Evaluate proxies on NASBench-101/201, NATS-Bench, TransNAS-Bench-101, ImageNet-1K CNNs, ViTs, and hardware-aware settings with latency/energy predictors.
- Source: Sec. 3, Fig. 5, Table 3

### Stage 4: Run Cross-Setting Comparisons

- Compare rank correlations in unconstrained spaces, top-5% constrained spaces, specific network families, large-scale tasks, ViTs, and Pareto-constrained search.
- Source: Sec. 4.1-4.4, Fig. 6-19, Table 4-6

### Stage 5: Distill Failure Modes and Future Directions

- Explain why `#Params` often works, when it fails, why current benchmarks are insufficient, and why customized proxies may be the more realistic next step.
- Source: Sec. 4.5, Sec. 5

## Pseudocode

```text
Algorithm: Zero-shot NAS Survey Evaluation Framework
Input: Search space S, proxy set P, benchmark/task set B, optional hardware constraints H
Output: Correlation reports, proxy rankings, design takeaways

1. Define proxy-quality criteria: expressive capacity, generalization, trainability.
   Source: Sec. 2.1
2. Partition candidate proxies into gradient-based and gradient-free groups.
   Source: Sec. 2.2, Sec. 2.3, Table 2
3. For each benchmark/task/hardware setting in B:
   3.1 Compute proxy scores for architectures at initialization.
       Source: Sec. 4, Inference from source
   3.2 Compare proxy scores against final accuracy using SPR/KT on all architectures and top-performing subsets.
       Source: Sec. 4.1, Fig. 6-14
   3.3 Under hardware constraints, trace proxy-selected Pareto candidates against ground truth.
       Source: Sec. 4.4, Fig. 18-19
4. Record where naive baselines (#Params/#FLOPs) remain stronger and where specialized proxies help.
   Source: Sec. 4.1-4.4
5. Summarize benchmark gaps, theory gaps, and directions for customized future proxies.
   Source: Sec. 4.5, Sec. 5
```

## Training Pipeline

1. This is not a trainable method in the usual sense; the paper evaluates initialization-time proxies.
2. Load a benchmark or model family and sample candidate architectures.
3. Compute proxy scores without full architecture training.
4. Compare those scores against eventual trained performance or against hardware-constrained Pareto fronts.

Sources:

- Sec. 3, Sec. 4, Table 4-6, Fig. 18-19

## Inference Pipeline

1. Pick a search space and optional hardware budget.
2. Compute the chosen zero-shot proxy on each candidate at initialization.
3. Use the proxy to rank or filter candidates before more expensive verification.
4. Validate top candidates with actual training/evaluation, especially in high-accuracy regions.

Sources:

- Sec. 2, Sec. 4.1, Sec. 4.4

## Complexity and Efficiency

- Time complexity: Not reported in closed form.
- Space complexity: Not reported in closed form.
- Runtime characteristics: Zero-shot proxy-based NAS is far cheaper than one-shot NAS; Table 6 reports search cost as low as `0.03` GPU hours for `#Params`, versus `200` GPU hours for a one-shot baseline.
- Scaling notes: Gradient-free proxies are cheaper than gradient-based ones because they avoid backward passes; however, lower cost does not imply better rank quality.

## Implementation Notes

- Code structure: `main.py` enumerates architectures from benchmark APIs and computes proxy scores.
- Proxy implementations: `measures/grad_norm.py`, `measures/snip.py`, `measures/grasp.py`, `measures/fisher.py`, `measures/jacob_cov.py`, `measures/synflow.py`.
- Additional utilities: NTK, Logdet, and Zen-score logic are wired through `main.py` and `measures/__init__.py`.
- External dependencies: NAS-Bench-101/201, NATS-Bench, `ptflops`, dataset loaders, and CUDA.
- Paper/code gap: the public repo is an evaluation toolkit plus paper list, not a turnkey reproduction of every table/figure end-to-end.

## Comparison to Related Methods

- Compared with [[One-shot NAS]]: zero-shot NAS avoids supernet training and is much cheaper, but ranking quality is weaker and less stable.
- Compared with [[Multi-shot NAS]]: zero-shot NAS is dramatically cheaper, but it relies on initialization-time proxies rather than trained candidate accuracy.
- Main advantage: gives a practical lens for deciding when a proxy is useful and when simple baselines already dominate.
- Main tradeoff: no single proxy emerges as a reliable universal winner across search spaces, tasks, and hardware constraints.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 5, Fig. 6-9, Fig. 17-19
- Key table(s): Table 2, Table 3, Table 4-6
- Key equation(s): Eq. (1)-(6), Eq. (10)-(20)
- Key algorithm(s): No single algorithm block; the contribution is a comparative evaluation framework assembled across Sec. 2-4

## References

- arXiv: https://arxiv.org/abs/2307.01998
- HTML: https://arxiv.org/html/2307.01998v3
- Code: https://github.com/SLDGroup/survey-zero-shot-nas
- Local implementation: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities

