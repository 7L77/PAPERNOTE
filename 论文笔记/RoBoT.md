---
title: "Robustifying and Boosting Training-Free Neural Architecture Search"
method_name: "RoBoT"
authors: [Zhenfeng He, Yao Shu, Zhongxiang Dai, Bryan Kian Hsiang Low]
year: 2024
venue: ICLR
tags: [nas, training-free-nas, bayesian-optimization, zero-cost-proxy, benchmark]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2403.07591v1
local_pdf: D:/PRO/essays/papers/Robustifying and Boosting Training-Free Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search
created: 2026-03-17
---

# Paper Note: RoBoT

## TL;DR
> RoBoT combines multiple training-free metrics with BO-optimized linear weights to get a more robust estimator, then spends remaining budget on greedy exploitation of top-ranked architectures to close the estimation gap.

## Metadata
| Item | Value |
|---|---|
| Paper | Robustifying and Boosting Training-Free Neural Architecture Search |
| Venue | ICLR 2024 |
| OpenReview | https://openreview.net/forum?id=qPloNoDJZn |
| arXiv | https://arxiv.org/abs/2403.07591 |
| Code | https://github.com/hzf1174/RoBoT |
| Local PDF | `D:/PRO/essays/papers/Robustifying and Boosting Training-Free Neural Architecture Search.pdf` |
| Local Code | `D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search` |

## Problem Setup
- Goal: make training-free NAS stable across diverse tasks and improve final selected architecture quality under a fixed search budget.
- RQ1: can we robustify unstable single training-free metrics across tasks?
- RQ2: after building a robust metric, how do we quantify and exploit the estimation gap between proxy score and true architecture performance?

## Core Contributions
1. Weighted ensemble of training-free metrics, with BO to optimize the weight vector for the current task.
2. Precision@T-based gap quantification and greedy exploitation over top-ranked candidates to boost final architecture selection.
3. Partial-monitoring-based analysis with a bound on expected ranking performance under mild assumptions.
4. Strong empirical results on NAS-Bench-201, TransNAS-Bench-101 (micro/macro), and DARTS search space.

## Method

### 1) Robust metric via weighted combination (Sec. 4.1)
The robust metric is:

\[
M(A; w) = \sum_{i=1}^{M} w_i M_i(A)
\]

with target weight:

\[
w^* = \arg\max_w f(A(w)), \quad A(w)=\arg\max_{A \in \mathcal{A}} M(A;w)
\]

Source: Sec. 4.1, Eq. (1).

### 2) BO exploration for weight optimization (Sec. 4.2, Alg. 1)
- BO iteratively proposes weight vectors.
- For each weight vector, RoBoT picks its top-scoring architecture and queries objective performance if not queried before.
- Best queried weight yields the robust estimator \(M(\cdot; \tilde{w}^*)\).

### 3) Precision@T and exploitation (Sec. 4.3, Alg. 2)
Precision@T:

\[
\rho_T(M,f)=\frac{|\{A\;|\;R_M(A)\le T \land R_f(A)\le T\}|}{T}
\]

Then use remaining budget for greedy search over top \(T-T_0\) architectures ranked by the robust metric.

Source: Sec. 4.3, Eq. (2), Eq. (3), Alg. 2.

### 4) Theory (Sec. 5)
- The paper maps Algorithm 1 to [[Partial Monitoring]].
- Under global observability-style conditions and BO strategy assumptions, they derive a bounded expected ranking for RoBoT's selected architecture.
- Key bound reported in Theorem 2 (Eq. 5).

## Key Results

### NAS-Bench-201 (Table 2)
- RoBoT: 94.36 / 73.51 / 46.34 (C10/C100/IN-16), search cost 3051 GPU-sec.
- Outperforms or matches best listed training-free/hybrid baselines at similar or lower cost than many training-based methods.

### TransNAS-Bench-101 (Table 3)
- Under budget 100, RoBoT achieves top-tier or best validation rankings across most micro and macro tasks.
- Example (micro): Scene 2, Object 1, Jigsaw 17, Segment 4, Normal 8 (lower is better).

### DARTS space ImageNet transfer (Table 4)
- RoBoT reports 24.1% top-1 error / 7.3% top-5 error, 0.6 GPU days search cost.
- Competitive against TE-NAS, HNAS, NASI-ADA, and many classical NAS baselines.

## Implementation Cross-check with Archived Code

Repository inspected:
`D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search`

Observed alignment:
1. Metric combination and min-max normalization are implemented in both `search_nb201.py` and `search_tnb101.py`.
2. BO searches over metric weights in \([-1,1]\), tracks best queried architecture-value pair, and records unique queried architectures (`T0` behavior).
3. Exploitation phase fills remaining budget by scanning top-ranked architectures under optimized weights.

Notable implementation detail:
1. Scripts use BO acquisition `ucb` directly; paper theory discussion mentions IDS conditions in analysis section, so practical code path is a simplified BO instantiation.
2. In benchmark scripts, objective feedback is tabular validation performance; in DARTS space, scripts train sampled architectures to obtain validation signal.

## Strengths
1. Clean separation between robustification (metric ensemble) and boosting (budgeted exploitation).
2. Practical: can reuse existing training-free metrics and benchmark tables.
3. Provides both empirical gains and explicit theoretical framing.

## Limitations
1. Dependence on available candidate pool quality and objective-query budget.
2. Theory relies on assumptions (e.g., observability-related conditions) that may not hold uniformly in real search spaces.
3. Weight optimization still introduces BO overhead and hyperparameter sensitivity.

## Related Concepts
- [[Training-free NAS]]
- [[Bayesian Optimization]]
- [[Precision@T]]
- [[Partial Monitoring]]
- [[Information Directed Sampling]]
- [[NAS-Bench-201]]
- [[TransNAS-Bench-101]]
- [[Differentiable Architecture Search]]
