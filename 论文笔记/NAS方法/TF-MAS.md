---
title: "TF-MAS"
type: method
source_paper: "TF-MAS: Training-free Mamba2 Architecture Search"
source_note: "[[TF-MAS]]"
authors: [Yi Fan, Yu-Bin Yang]
year: 2025
venue: NeurIPS
tags: [nas-method, nas, training-free-nas, mamba2]
created: 2026-03-16
updated: 2026-03-16
---

# TF-MAS

## One-line Summary
> TF-MAS is a training-free NAS proxy for Mamba2 that estimates block-wise transformation matrices (`U->X/B/C`) and scores architectures by multiplying nuclear norms of those matrices and their gradients.

## Source
- Paper title: TF-MAS: Training-free Mamba2 Architecture Search
- Local PDF: `D:/PRO/essays/papers/TF-MAS Training-free Mamba2 Architecture Search.pdf`
- Code: https://github.com/fanyi-plus/tf-nas
- Paper note: [[TF-MAS]]

## Applicable Scenarios
- Problem type: Search Mamba2-like architectures under compute budgets without full candidate training.
- Assumptions: Candidate models follow Mamba2 block structure and SSD-style computation.
- Data regime: Zero-shot proxy evaluation plus optional evolutionary search.
- Scale / constraints: Large architecture sets where full training is too expensive.
- Why it fits: It derives Mamba-specific proxy terms rather than reusing CNN/Transformer proxies directly.

## Not a Good Fit When
- The model family is far from Mamba2 (different block semantics, no SSD correspondence).
- You need fully reproducible open-source implementation right now (official code is not fully released yet).
- You require high absolute ranking reliability on every target metric without follow-up validation.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture `A`, sampled network input `D`, intermediate tensors `U/X/B/C`, output FC weights.
- Outputs: Scalar proxy value `TF-MAS` for ranking candidates.
- Objective: Maximize correlation (Kendall's Tau) between proxy ranking and true performance ranking.
- Core assumptions: Rank-collapse behavior in stacked SSD is informative about final architecture quality.

## Method Breakdown

### Stage 1: Build block-wise transformation matrices
- For each block, solve `U W_X = X`, similarly for `W_B` and `W_C`.
- Use three shape-aware cases: inverse (`T=W`), pseudoinverse min-norm (`T<W`), least-squares approximation (`T>W`).
- Source: Sec. 3.1, Eq. (2)-(5).

### Stage 2: Compute gradients and proxy terms
- Backprop once to obtain gradients for `X/B/C/out`-related quantities.
- Derive gradients for `W_X/W_B/W_C` via chain rule rather than direct parameter gradients.
- Source: Sec. 3.1, Eq. (6), Appendix D Algorithm 1.

### Stage 3: Aggregate TF-MAS score
- Sum across layers and matrix groups (`X/B/C/out`) using product of nuclear norms:
  `||W||_nuc * ||dL/dW||_nuc`.
- Source: Eq. (6), Appendix D Algorithm 1.

### Stage 4: Search-space construction and evolutionary search
- Define AHs: `D/W/N/H`, solve scaling factor `k` via budget equation.
- Build SSMamba2 or VWSSMamba2, then run evolutionary search under budget constraints.
- Source: Sec. 3.2, Eq. (7), Sec. 4.2, Appendix G.

## Pseudocode
```text
Algorithm: TF-MAS
Input: Architecture A, input batch D
Output: Proxy score s

1. Initialize candidate A and collect block output weights W_out.
   Source: Appendix D, Alg. 1 (lines 1-2)
2. Forward pass to extract U, X, B, C for each block.
   Source: Appendix D, Alg. 1 (line 2)
3. Backward pass to obtain gradients wrt X/B/C and W_out.
   Source: Appendix D, Alg. 1 (line 3)
4. Group blocks by compatible tensor shapes; batch-concatenate equations.
   Source: Appendix D, Alg. 1 (lines 4-8)
5. For each group, solve W via inverse or SVD-pseudoinverse depending on T vs W.
   Source: Sec. 3.1 Eq. (2)-(5), Appendix D lines 9-16
6. Recover per-block W_X/W_B/W_C and derive their gradients through U^T * dL/dX style relations.
   Source: Sec. 3.1, Appendix D lines 17-18
7. Accumulate s = Σ_i Σ_{x in {X,B,C,out}} ||W_x^(i)||_nuc * ||dL/dW_x^(i)||_nuc.
   Source: Eq. (6), Appendix D line 19
8. Return s.
   Source: Appendix D line 20
```

## Training Pipeline
1. Create NASBench-style candidate sets from pretrained Mamba2 checkpoints (weight entanglement setup).
2. For each candidate, compute TF-MAS without full training.
3. Use proxy-guided evolutionary search to pick architectures.
4. Retrain selected architectures from scratch and evaluate.

Sources:
- Sec. 4.1, Sec. 4.2
- Table 1-3, Appendix G

## Inference Pipeline
1. Sample candidate architecture within AH ranges.
2. Compute TF-MAS score by the above proxy pipeline.
3. Rank/select candidates and pass top ones to real training.

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4.2

## Complexity and Efficiency
- Time complexity (one block): `O(WHP min(W,P) + WHN min(W,N))`.
- Space complexity: Not explicitly given as a closed form.
- Runtime characteristics: Proxy computation remains practical; search on 4xV100 reported as 0.6-0.7 day depending on search space.
- Scaling notes: Authors claim near-linear growth when any of `W/N/H/P` increases.

Sources:
- Appendix C.7
- Sec. 4.2

## Implementation Notes
- The method critically depends on solving `AW=B` for transformation matrices, not using FC weights directly.
- Appendix pseudocode includes shape-based batching before SVD/pseudoinverse to improve throughput.
- Search constraints are enforced by parameter upper bound (`<=130M` in reported setup).
- Block-wise evolution (BWE) computes layer-wise proxy and mutates low-score layers first.
- Official repository exists locally but currently exposes only a placeholder README (full modules not yet released).

## Comparison to Related Methods
- Compared with DSS++-style Transformer proxies: TF-MAS adapts rank-collapse logic to SSD/Mamba2 internals.
- Compared with generic CNN proxies (e.g., GraSP/SNIP variants): TF-MAS is architecture-matched and shows stronger correlation in reported Mamba2 benches.
- Main advantage: First Mamba-tailored training-free proxy with both correlation and search-result validation.
- Main tradeoff: Current public-code incompleteness and still-moderate correlation on some datasets.

## Evidence and Traceability
- Key figure(s): Figure 1, Figure 2, Figure 3.
- Key table(s): Table 1 (proxy correlation), Table 2 (search results), Table 3 (wfc ablation), Table 4-6 (analysis/stability).
- Key equation(s): Eq. (2)-(7), Eq. (17) in appendix.
- Key algorithm(s): Appendix D, Algorithm 1.

## References
- Paper note: [[TF-MAS]]
- Code: https://github.com/fanyi-plus/tf-nas
- Local implementation: D:/PRO/essays/code_depots/TF-MAS Training-free Mamba2 Architecture Search
