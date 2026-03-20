---
title: "Per-Architecture Training-Free Metric Optimization for Neural Architecture Search"
method_name: "PO-NAS"
authors: [Anonymous Author(s)]
year: 2025
venue: "NeurIPS 2025 (under review submission)"
tags: [nas, training-free-nas, zero-cost-proxy, surrogate-model, evolutionary-search]
zotero_collection: ""
image_source: online
arxiv_html: ""
project_page: "https://anonymous.4open.science/r/PO-NAS-2953"
local_pdf: D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf
local_code: "Not archived (anonymous repository not found as of 2026-03-16)"
created: 2026-03-16
---

# Paper Note: PO-NAS

## Meta
| Item | Content |
|---|---|
| Paper | Per-Architecture Training-Free Metric Optimization for Neural Architecture Search |
| Status | Submitted to NeurIPS 2025 (anonymous submission PDF) |
| Code link in paper | https://anonymous.4open.science/r/PO-NAS-2953 |
| Local PDF | `D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf` |
| Local code | Not archived (repository URL not clonable on 2026-03-16) |

## One-line Summary
> PO-NAS learns per-architecture weights over multiple training-free metrics via a surrogate model and combines this with BO + evolutionary search to improve NAS ranking quality under small real-training budgets.

## Core Contributions
1. Proposes architecture-specific metric fusion instead of global metric weighting, using
   \(S(A;w_A)=\sum_i w_{A,i}\tilde Z_i(A)\) (Eq. 1).
2. Builds a surrogate with an encoder + metric predictor + cross-attention weight generator to learn architecture-conditional metric weights (Sec. 3.3-3.4).
3. Introduces a BO-driven loop with pairwise ranking-oriented losses (Eq. 6-8), then couples it with an evolutionary stage for broader exploration (Sec. 3.2, 3.5).
4. Reports strong benchmark results on NAS-Bench-201, DARTS/ImageNet, and TransNAS-Bench-101 (Table 1-3).

## Problem Context
### Target problem
- Improve architecture ranking in [[Training-free NAS]] when direct training-based NAS is too expensive.

### Prior limitation
- Single [[Zero-Cost Proxy]] metrics transfer inconsistently across tasks.
- Existing hybrid methods often optimize a *global* metric combination, ignoring architecture-level sensitivity differences.

### Why PO-NAS
- PO-NAS learns metric weights per architecture using limited real feedback, then scales exploration using predicted scores.

## Method Details
### 1) Per-architecture scoring and optimization objective
Given K training-free metrics:

$$
S(A; w_A) = \sum_{i=1}^{K} w_{A,i}\,\tilde Z_i(A)
$$

- Source: Eq. (1), Sec. 3.1.
- \(\tilde Z_i\): normalized metric value.
- \(w_A\): architecture-specific weight vector (L1-normalized in paper text).

Weight learning is formulated by maximizing [[Kendall's Tau]] rank consistency between score ranking and true performance over evaluated candidates:

$$
w_A^{(t+1)} = \arg\max_{w_A} \tau\big(\{S(A;w_A^{(t)})\}_{A\in A_t},\{f(A)\}_{A\in A_t}\big)
$$

- Source: Eq. (2), Sec. 3.1.

### 2) Encoder pretraining
- Uses a 2-layer [[Graph Attention Network]] to encode architecture graphs into embeddings (Sec. 3.3, Fig. 2).
- Uses node-mask reconstruction + metric prediction pretraining:

$$
\mathcal{L}_{recon} = \frac{1}{|V_m|}\sum_{v\in V_m}\|\hat x_v-x_v\|_2^2,
\quad
\mathcal{L}_{metric} = \frac{1}{K}\sum_{i=1}^{K}\|P_z^i(h_G)-Z_i(G)\|_2^2
$$

- Source: Eq. (3), Eq. (4).

### 3) Surrogate score with signed metric effects
After normalization, PO-NAS splits weights into positive/negative activations and computes:

$$
\hat S = \sum_{i=1}^{K}\big(\hat w_i^+\hat Z_i + \hat w_i^- (1-\hat Z_i)\big)
$$

- Source: Eq. (5), Sec. 3.4.
- Intuition: preserve both positive and negative correlation behavior between a metric and performance.

Surrogate optimization uses three losses:
1. Alignment loss on pairwise score/performance gap distributions with threshold mask \(T_{th}\) (Eq. 6).
2. Correlation loss \(\mathcal{L}_{corr}=1-\rho(\hat S,f)\) using Pearson correlation (Eq. 7).
3. Direction loss \(\mathcal{L}_{dir}=\mathbb{E}[\mathrm{ReLU}(-\Delta_{pred}\Delta_{true})]\) (Eq. 8).

- Source: Sec. 3.4, Eq. (6)-(8).

### 4) Search loop and evolution
- Main loop: initialization -> pretraining -> BO stage -> optional evolution stage (Algorithm 1).
- Evolution stage includes shortest-operation-path crossover and neighborhood traversal mutation (Appendix A.2-A.4, Algorithm 2).
- Pair score in evolution:

$$
S_{pair} = N\,\tilde S_{cost} + (1-N)\,\tilde S_{pre}
$$

- Source: Eq. (9), Appendix A.4.
- \(N\) is exploration weight: high early for exploration, lower later for exploitation.

## Key Experimental Evidence
### NAS-Bench-201 (Table 1)
- PO-NAS: **94.12±0.22 / 73.51±0.00 / 46.71±0.12** (CIFAR-10 / CIFAR-100 / ImageNet-16-120), search cost 3162 GPU sec.
- Versus RoBoT: similar C100, PO-NAS higher on C10 and IN-16.

### DARTS on ImageNet (Table 2)
- PO-NAS: **23.9 top-1 error / 7.1 top-5 error**, 6.3M params, 0.64 GPU days.
- Competitive or better than listed hybrid/training-free baselines in top-1 error.

### TransNAS-Bench-101 (Table 3)
- Micro and Macro settings both show PO-NAS near top or best across multiple tasks.
- Macro block reports strong gains over "Training-free (Avg./Best)" and competitive gains over RoBoT/HNAS.

## Implementation Details Worth Reproducing
1. Six base metrics: grad_norm, snip, grasp, fisher, synflow, jacob_cov (Sec. 4.1, App. B.2).
2. Pretraining includes architecture masking and 100-epoch schedule (App. B.2).
3. BO stage uses loss threshold and difference threshold \(T_{th}\) (default around 0.1 in appendix settings).
4. DARTS setup uses 10k initial architectures, limited true-training budget (25 for CIFAR, 10 for ImageNet), and starts evolution later in BO stage.

## Critical View
### Strengths
1. Tackles a real limitation in metric fusion: architecture-wise heterogeneity.
2. Hybrid design is practical: cheap metrics + sparse true training + guided search.
3. Evolution module is designed for large spaces where BO-only candidate refresh may be narrow.

### Limitations
1. Surrogate stability remains a known issue (paper itself discusses this).
2. Method complexity is higher than single-proxy pipelines (encoder, predictor, attention, multiple losses, evolution logic).
3. True reproducibility is constrained right now because anonymous code link is not publicly clonable.

### Follow-up Ideas
1. Try cluster-level metric weighting (paper's own future-work direction) as a stability/performance tradeoff.
2. Test robustness to metric subset changes per search space/task.
3. Compare against newer 2025-2026 proxy-fusion baselines once public implementations are available.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Surrogate Predictor]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
- [[Bayesian Optimization]]
- [[Evolutionary Neural Architecture Search]]
- [[Graph Attention Network]]
- [[Cross-Attention]]
- [[Cell-based Search Space]]
- [[NAS-Bench-201]]
