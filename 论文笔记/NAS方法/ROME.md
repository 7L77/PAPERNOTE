---
title: "ROME"
type: method
source_paper: "ROME: Robustifying Memory-Efficient NAS via Topology Disentanglement and Gradient Accumulation"
source_note: "[[ROME]]"
authors: [Xiaoxing Wang, Xiangxiang Chu, Yuda Fan, Zhexi Zhang, Bo Zhang, Xiaokang Yang, Junchi Yan]
year: 2023
venue: ICCV
tags: [nas-method, differentiable-nas, single-path-nas, robustness]
created: 2026-03-14
updated: 2026-03-14
---

# ROME

## One-line Summary
> ROME stabilizes single-path differentiable NAS by decoupling edge-topology selection from operation selection, then reducing bi-level optimization noise via two gradient-accumulation loops.

## Source
- Paper: [ROME: Robustifying Memory-Efficient NAS via Topology Disentanglement and Gradient Accumulation](https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html)
- HTML: https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html
- Code: Not linked in paper/CVF/arXiv
- Paper note: [[ROME]]

## Applicable Scenarios
- Problem type: Cell-based differentiable NAS where collapse to parameter-free operations is observed.
- Assumptions: Final architecture must satisfy DARTS-style topology constraints (each intermediate node with in-degree 2).
- Data regime: Supernet search with train/val split for bi-level optimization.
- Scale / constraints: Memory-constrained search where full-path DARTS is too expensive.
- Why it fits: Single-path forward/backward plus strict edge sampling reduces memory and mismatch between search/evaluation.

## Not a Good Fit When
- The target model family is not DAG/cell based and has no in-degree style topology constraints.
- You need a one-stage search method without bi-level optimization overhead.
- You cannot afford repeated subnetwork sampling per iteration (K-sampling accumulation).

## Inputs, Outputs, and Objective
- Inputs: Search-space DAG, operation set per edge, supernet weights `omega`, architecture weights `alpha` (ops) and `beta` (edges), sampling number `K`.
- Outputs: Discrete architecture `z*` maximizing `p(z; alpha, beta)`.
- Objective: Minimize expected validation loss under sampled architectures while training supernet weights on train loss.
- Core assumptions: Collapse is mainly caused by topology inconsistency and insufficient stochastic sampling.

## Method Breakdown

### Stage 1: Topology-operation disentanglement
- Introduce edge indicator `B_{i,j}` and operation indicator `A^o_{i,j}`.
- Enforce each intermediate node has exactly two predecessors.
- Source: Sec. 3.3, Eq. (1-3).

### Stage 2: Topology sampling with Gumbel reparameterization
- ROME-v1: sample edge pairs by enumerating combinations.
- ROME-v2: directly choose top-2 edges per node using Gumbel-Top2.
- Source: Sec. 3.4.1-3.4.2, Eq. (4-8), Sec. 3.5.

### Stage 3: Bi-level optimization with two accumulation loops
- Sample `K` subnetworks to update architecture parameters on validation split.
- Sample another `K` subnetworks to update operation weights on train split.
- Source: Sec. 3.6, Eq. (9-12), Algorithm 1.

## Pseudocode

```text
Algorithm: ROME (v2 default)
Input: Supernet weights omega, architecture weights alpha (ops), beta (edges), sampling count K, iterations T
Output: Final architecture z*

1. For t = 1..T, sample Ds (val split) and Dt (train split).
   Source: Alg. 1 line 2
2. Repeat k = 1..K: sample topology B using Gumbel-Top2 and operations A using Gumbel-Max/Softmax, get z_k.
   Source: Sec. 3.4.2, Eq. (7-8), Eq. (3), Alg. 1 line 3-6
3. Update alpha and beta by averaging gradients of L_val(omega, z_k) over K samples.
   Source: Eq. (11), Alg. 1 line 7
4. Repeat k = 1..K: resample z'_k with same sampling rules.
   Source: Alg. 1 line 8-11
5. Update omega by accumulating gradients of L_train(omega, z'_k).
   Source: Eq. (12), Alg. 1 line 12
6. After search, decode z* = argmax_z p(z; alpha, beta).
   Source: Eq. (9), Alg. 1 line 14
```

## Training Pipeline
1. Build DARTS-style supernet (8 cells, initial channels 16 for search).
2. Set `K=7` by default and train search for 50 epochs on CIFAR-10 setting.
3. Alternate architecture update (`alpha`,`beta`) and operation update (`omega`) with separate sampled subnet batches.
4. Decode final architecture and fully train for evaluation.

Sources:
- Sec. 4.1
- Algorithm 1

## Inference Pipeline
1. Use decoded architecture `z*` (not the supernet) for standard training/inference.
2. For CIFAR evaluation, train discovered architecture under DARTS-style protocol.
3. For ImageNet transfer/direct search, follow paper-reported training settings.

Sources:
- Sec. 4.1, Sec. 4.3
- Inference from source (serving pipeline is not separately formalized)

## Complexity and Efficiency
- Time complexity: Not reported as closed-form; per-iteration cost scales with sampling number `K`.
- Space complexity: Lower than GDAS/PC-DARTS in reported setup due strict two-edge sampling.
- Runtime characteristics: 0.3 GPU-days for CIFAR search in S0; supports direct ImageNet search at low cost.
- Scaling notes: Accuracy improves as `K` increases (Table 5), then saturates around `K=7`.

## Implementation Notes
- Operation sampling and edge sampling are both differentiable through Gumbel reparameterization.
- ROME-v2 is preferred in paper due better efficiency and robustness than v1.
- Two different data batches are used in each iteration for bi-level updates.
- Key hyperparameters (search setting): SGD for `omega` (lr 0.05, momentum 0.9), Adam for architecture weights (lr 3e-4), `K=7`.
- Practical gotcha: Without official released code link in paper page, exact engineering details beyond manuscript remain paper-derived.

## Comparison to Related Methods
- Compared with [[GDAS]]: ROME adds explicit topology disentanglement and dual accumulation, reducing collapse.
- Compared with [[DARTS]]: ROME is single-path and far more memory efficient.
- Main advantage: Better robustness across repeated search runs and hard benchmarks.
- Main tradeoff: Additional sampling loops increase implementation complexity.

## Evidence and Traceability
- Key figure(s): Fig. 1 (framework), Fig. 2-3 (collapse evidence), Fig. 4-5 (hard-space robustness).
- Key table(s): Table 1-7.
- Key equation(s): Eq. (1-3), Eq. (7-8), Eq. (9-12).
- Key algorithm(s): Algorithm 1.

## References
- arXiv: Not explicitly linked on CVF paper page
- HTML: https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html
- Code: Not linked in paper/CVF/arXiv
- Local implementation: Not archived

