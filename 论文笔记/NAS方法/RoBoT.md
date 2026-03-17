---
title: "RoBoT"
type: method
source_paper: "Robustifying and Boosting Training-Free Neural Architecture Search"
source_note: "[[RoBoT]]"
authors: [Zhenfeng He, Yao Shu, Zhongxiang Dai, Bryan Kian Hsiang Low]
year: 2024
venue: ICLR
tags: [nas-method, training-free-nas, bayesian-optimization]
created: 2026-03-17
updated: 2026-03-17
---

# RoBoT

## One-line Summary
> RoBoT first learns a robust weighted ensemble of training-free metrics with Bayesian optimization, then uses remaining budget to greedily exploit top-ranked architectures for better final search outcomes.

## Source
- Paper: [Robustifying and Boosting Training-Free Neural Architecture Search](https://arxiv.org/abs/2403.07591)
- HTML: https://arxiv.org/html/2403.07591v1
- Code: https://github.com/hzf1174/RoBoT
- Paper note: [[RoBoT]]

## Applicable Scenarios
- Problem type: architecture ranking and selection with a fixed expensive evaluation budget.
- Assumptions: multiple training-free metrics exist and their weighted combination can better align with true performance.
- Data regime: supervised image tasks with benchmark tabular data or trainable candidate architectures.
- Scale / constraints: large candidate pool where full training for all candidates is infeasible.
- Why it fits: separates cheap proxy aggregation from expensive objective queries, and allocates budget to both exploration and exploitation.

## Not a Good Fit When
- No reliable training-free metrics are available for the search space.
- Candidate pool is tiny, so BO + exploitation overhead offers little gain.
- Objective signal is highly noisy or non-stationary across repeated evaluations.

## Inputs, Outputs, and Objective
- Inputs: candidate set \(\mathcal{A}\), training-free metric set \(\mathcal{M}\), objective metric \(f\), search budget \(T\).
- Outputs: selected architecture \(\tilde{A}^*_{M,T}\), optimized weight vector \(\tilde{w}^*\).
- Objective: maximize true architecture quality under constrained objective-query budget.
- Core assumptions: weighted proxy ranking contains top-performing architectures that can be surfaced by limited exploration and greedy exploitation.

## Method Breakdown

### Stage 1: Build weighted proxy metric
- Define \(M(A;w)=\sum_i w_i M_i(A)\).
- Each weight vector maps to a top-ranked architecture candidate.
- Source: Sec. 4.1, Eq. (1).

### Stage 2: BO exploration over weight vectors
- BO iteratively proposes \(w_t\), evaluates top architecture induced by \(w_t\), and records queried observations.
- Best observed \(w\) yields robust estimator \(M(\cdot;\tilde{w}^*)\).
- Source: Sec. 4.2, Alg. 1.

### Stage 3: Quantify estimation gap by Precision@T
- Use \(\rho_T(M,f)\) to measure overlap between top-T proxy ranking and top-T true ranking.
- Source: Sec. 4.3, Eq. (2), Theorem 1.

### Stage 4: Greedy exploitation with remaining budget
- Let \(T_0\) be number of distinct architectures queried in exploration.
- Use top \(T-T_0\) architectures under \(M(\cdot;\tilde{w}^*)\) for greedy objective querying.
- Source: Sec. 4.3, Alg. 2.

## Pseudocode
```text
Algorithm: RoBoT
Input: Objective metric f, training-free metrics M={M_i}, architecture pool A, budget T
Output: Selected architecture A_tilde_star, robust weight vector w_tilde_star

1. Define combined metric M(A; w) = sum_i w_i * M_i(A).
   Source: Sec. 4.1, Eq. (1)
2. Run BO over weight vectors:
   - Propose w_t, rank A by M(A; w_t), select top architecture A(w_t),
   - Query f(A(w_t)) if unseen, otherwise reuse cached value.
   Source: Sec. 4.2, Alg. 1
3. Select best queried weight vector w_tilde_star.
   Source: Alg. 1, line 14
4. Compute robust ranking R_{M(.; w_tilde_star)} and count distinct queried architectures T0.
   Source: Sec. 4.3, Alg. 2
5. Greedily query top (T - T0) unqueried architectures under robust ranking.
   Source: Sec. 4.3, Alg. 2
6. Return best architecture observed across exploration + exploitation.
   Source: Sec. 4.3, Eq. (3), Alg. 2
```

## Training Pipeline
1. Collect per-architecture training-free metric scores.
2. Normalize metric values (code uses min-max normalization per metric).
3. Run BO exploration on metric weights.
4. Run greedy exploitation on robust metric ranking.
5. Evaluate selected architecture on target benchmark protocol.

Sources:
- Sec. 4.1-4.3
- `search_nb201.py`
- `search_tnb101.py`
- `darts_space/search.py`

## Inference Pipeline
1. For a new NAS task with prepared candidate pool and metric scores, run BO to get \(\tilde{w}^*\).
2. Rank candidates by \(M(\cdot;\tilde{w}^*)\).
3. Allocate remaining budget to top-ranked candidates and keep best observed one.

Sources:
- Sec. 4.2-4.3
- Alg. 1, Alg. 2

## Complexity and Efficiency
- Time complexity: not given as a closed form in the paper for full pipeline.
- Practical compute profile:
  - proxy scoring is cheap relative to objective queries;
  - objective query count is bounded by budget \(T\);
  - robust ranking per BO step is linear in number of architectures and metrics.
- Search efficiency evidence: strong benchmark performance with low search cost (e.g., Table 2, Table 4).

## Implementation Notes
- Core scripts:
  - `search_nb201.py`
  - `search_tnb101.py`
  - `darts_space/search.py`
- BO setup in code:
  - metric weight bounds set to \([-1, 1]\),
  - acquisition used in scripts is `ucb`.
- Exploitation logic:
  - code explicitly appends highest-ranked unseen architectures until budget is filled.
- Data dependency:
  - NAS-Bench-201 and TransNAS-Bench-101 scripts rely on precomputed training-free metric files.
- Paper-code caveat:
  - theoretical section discusses IDS conditions, while released scripts instantiate standard BO with UCB.

## Comparison to Related Methods
- Compared with single [[Training-free NAS]] metrics:
  - RoBoT improves robustness across tasks by weighted ensembling instead of picking one metric.
- Compared with pure exploration:
  - RoBoT adds explicit exploitation to harvest estimation-gap gains.
- Main advantage: robust cross-task behavior plus better budget utilization.
- Main tradeoff: extra BO tuning and dependence on candidate metric quality.

## Evidence and Traceability
- Key figure(s): Fig. 1-3, Fig. 5-10.
- Key table(s): Table 1-4, Table 8-9.
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (5).
- Key algorithm(s): Algorithm 1, Algorithm 2.

## References
- arXiv: https://arxiv.org/abs/2403.07591
- HTML: https://arxiv.org/html/2403.07591v1
- Code: https://github.com/hzf1174/RoBoT
- Local implementation: D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search
