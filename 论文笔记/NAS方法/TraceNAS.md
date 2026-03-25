---
title: "TraceNAS"
type: method
source_paper: "TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation"
source_note: "[[TraceNAS]]"
authors: [Prajna G. Malettira, Manish Nagaraj, Arjun Roy, Shubham Negi, Kaushik Roy]
year: 2026
venue: arXiv
tags: [nas-method, llm-pruning, training-free-nas, zero-shot-proxy]
created: 2026-03-23
updated: 2026-03-23
---

# TraceNAS

## One-line Summary
> TraceNAS is a training-free NAS method for LLM structured pruning that ranks non-uniform depth-width candidates by sparsity-weighted Pearson alignment between candidate and base-model gradient traces.

## Source
- Paper: [TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation](https://arxiv.org/abs/2602.02891v1)
- HTML: https://arxiv.org/html/2602.02891v1
- Code: Not publicly released (paper mentions anonymous repo during review)
- Paper note: [[TraceNAS]]

## Applicable Scenarios
- Problem type: Joint depth-width structured pruning for pretrained LLMs.
- Assumptions: Good candidates should preserve functional inheritance with the pretrained base model.
- Data regime: Small calibration set for zero-shot ranking + optional post-pruning continued pretraining (CPT).
- Scale / constraints: Large-model settings where search-time training is too expensive.
- Why it fits: Uses first-order gradient alignment proxy with low-rank traces, avoiding training-aware search loops.

## Not a Good Fit When
- You need hardware-aware multi-objective optimization directly in the search objective.
- The deployment requires strict end-to-end latency optimization during search (not only parameter budget).
- You cannot afford any calibration forward/backward passes at search time.

## Inputs, Outputs, and Objective
- Inputs: Pretrained super-network `M_base`, parameter budget `C`, calibration set `B`, candidate encoding `(d, kappa)`.
- Outputs: Best pruned architecture `M_sub_hat` under budget.
- Objective: Maximize
  `Phi(M_sub, M_base)` subject to `P(M_sub) <= C`.
- Core assumptions: Gradient-direction alignment with the base model is a proxy for post-pruning recovery potential.

## Method Breakdown

### Stage 1: Candidate Encoding and Realization
- Encode each candidate with depth mask `d` and per-layer width retention `kappa_l=(r_attn, r_mlp)`.
- Realize width masks using activation-weighted saliency (`|W| * ||X||_2`) and in-place masking on base weights.
- Source: Sec. 3.2, Sec. 3.3, Fig. 2.

### Stage 2: Functional Anchor and Low-rank Gradient Traces
- Compute base gradient trace:
  `g_base = E_{b in B}[grad_theta L(M_base(b;theta))]`.
- Compute candidate trace `g_sub` in LoRA-induced low-rank subspace for memory efficiency.
- Source: Sec. 3.4.

### Stage 3: Proxy Scoring
- Per active layer, compute Pearson correlation `rho^(l)` between standardized `g_sub^(l)` and `g_base^(l)`.
- Aggregate correlations with sparsity weights:
  `Phi = sum_attn r_attn^(l) rho^(l) + sum_mlp r_mlp^(l) rho^(l)`.
- Source: Sec. 3.4 Eq. (1)-(2).

### Stage 4: Evolutionary Search
- Select top-k elites by `Phi`, then apply crossover/mutation over both depth and width encodings.
- Iterate and return the best candidate satisfying budget.
- Source: Sec. 3.5, Appendix A.4 Algorithm 1.

## Pseudocode

```text
Algorithm: TraceNAS
Input: Pretrained model M_base, budget C, calibration set B, elite size k, iterations T
Output: Best pruned architecture M_sub_hat

1. Attach low-rank adapters to M_base and compute g_base over B.
   Source: Sec. 3.4
2. Initialize population P0 with depth masks d and width ratios kappa.
   Source: Sec. 3.2, Sec. 3.5
3. For t = 1..T:
   3.1 For each candidate (d, kappa) in Pt:
       - Realize in-place structural masks on M_base.
       - If params exceed C, assign very low score.
       - Compute g_sub over B.
       - For each active layer l, compute rho^(l) using Pearson correlation.
       - Compute Phi via sparsity-weighted aggregation.
       Source: Sec. 3.3-3.4, Eq. (1)-(2)
   3.2 Keep top-k elites and generate offspring by crossover/mutation.
       Source: Sec. 3.5, Appendix A.4 Alg. 1
4. Return highest-scoring candidate in final population.
   Source: Appendix A.4 Alg. 1
```

## Training Pipeline
1. Run evolutionary search with proxy scoring only (no search-time model training).
2. Select top candidate architectures under parameter targets (e.g., 2.7B/4.6B/8.4B).
3. Perform post-pruning CPT on selected model(s).

Sources:
- Sec. 4.1
- Tab. 2-3

## Inference Pipeline
1. Deploy pruned architecture directly after CPT.
2. Evaluate on reasoning/commonsense suites (MMLU, PIQA, ARC, HellaSwag, etc.).
3. Optionally profile prefill/decode speed and memory.

Sources:
- Sec. 4.3
- Appendix D.1

## Complexity and Efficiency
- Time complexity: Per-candidate scoring uses first-order gradients plus O(d^2)-style mask realization; avoids O(d^3) second-order reconstructions.
- Space complexity: Reduced by storing low-rank gradient traces instead of full-rank gradients.
- Runtime characteristics: Search completed in ~8.5 GPU-hours on A100 baseline (or ~2 hours on H200 in setup).
- Scaling notes: Proxy remains stable across calibration size, context length, and gradient rank (Sec. 4.2, Appendix C.3).

## Implementation Notes
- Search hyperparameters (reported): population=30, elite=10, iterations=50, crossover=0.7, mutation=0.2.
- Candidate scoring budget: 65,536 calibration tokens per candidate.
- GQA models: do not prune `Wk/Wv` to preserve KV-cache compatibility.
- MLP dimensions are rounded to multiples of 32 for tensor efficiency.
- Code status: method note is paper-derived because public official repo is unavailable.

## Comparison to Related Methods
- Compared with [[DarwinLM]]:
  TraceNAS avoids search-time training and uses gradient-trace proxy; lower search overhead with competitive recovered accuracy.
- Compared with [[ShearedLLaMA]]:
  TraceNAS performs non-uniform joint depth-width search rather than fixed/less-coupled pruning patterns.
- Main advantage: Search efficiency and ranking fidelity for recovery potential.
- Main tradeoff: Requires calibration gradients and still depends on downstream CPT for full recovery.

## Evidence and Traceability
- Key figure(s): Fig. 1 (search efficiency), Fig. 2 (framework), Fig. 3 (proxy stability).
- Key table(s): Tab. 1 (proxy correlations), Tab. 2-3 (main pruning results).
- Key equation(s): Eq. (1) Pearson layer alignment; Eq. (2) sparsity-weighted aggregation.
- Key algorithm(s): Appendix A.4 Algorithm 1.

## References
- arXiv: https://arxiv.org/abs/2602.02891v1
- HTML: https://arxiv.org/html/2602.02891v1
- Code: Not publicly available at time of note creation
- Local implementation: Not archived
