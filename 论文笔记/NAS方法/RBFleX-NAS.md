---
title: "RBFleX-NAS"
type: method
source_paper: "RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection"
source_note: "[[RBFleX-NAS]]"
authors: [Tomomasa Yamasaki, Zhehui Wang, Tao Luo, Niangjun Chen, Bo Wang]
year: 2025
venue: TNNLS
tags: [nas-method, training-free-nas, rbf-kernel, activation-search]
created: 2026-03-16
updated: 2026-03-16
---

# RBFleX-NAS

## One-line Summary

> RBFleX-NAS is a training-free NAS scoring method that combines RBF-kernel similarities from activation outputs and final-layer input feature maps, with HDA-based automatic kernel hyperparameter detection.

## Source

- Paper: [RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection](https://arxiv.org/abs/2503.22733)
- HTML: https://arxiv.org/html/2503.22733v3
- Code: https://github.com/Edge-AI-Acceleration-Lab/RBFleX-NAS
- Paper note: [[RBFleX-NAS]]

## Applicable Scenarios

- Problem type: Training-free ranking of candidate architectures before expensive full training.
- Assumptions: Better architectures induce lower cross-sample similarity in both activation outputs and last-layer input feature maps.
- Data regime: Mini-batch based image/text inputs; label-free scoring.
- Scale / constraints: Best for benchmark-driven candidate pools where quick top-k screening is needed.
- Why it fits: Uses two complementary representation views (`X` and `Y`) and avoids manual gamma tuning via HDA.

## Not a Good Fit When

- You need calibrated absolute accuracy prediction, not ranking.
- Candidate models are too large to extract all activation outputs efficiently.
- The search setting has no stable mini-batch distribution for reliable similarity estimation.

## Inputs, Outputs, and Objective

- Inputs: Candidate network `f`, mini-batch inputs, detected `gamma_k` and `gamma_q`.
- Outputs: Scalar score used for ranking candidate architectures.
- Objective: Rank candidates so high-performing architectures are selected early for final training.
- Core assumptions: Cross-sample representation geometry at initialization correlates with final trained quality.

## Method Breakdown

### Stage 1: Collect Two Representation Matrices

- Build `X` from flattened outputs of activation layers for each input image.
- Build `Y` from flattened feature map entering the final layer.
- Source: Sec. III-A, Fig. 4, Fig. 5.

### Stage 2: Column-wise Normalization

- Normalize each column of `X` and `Y` to `[0,1]` to preserve row-level relation.
- Source: Sec. III-A, Eq. (1).

### Stage 3: Build Dual RBF Similarity Matrices

- Compute `K_ij = exp(-gamma_k ||x_i-x_j||^2)` and `Q_ij = exp(-gamma_q ||y_i-y_j||^2)`.
- Source: Sec. III-A, Eq. (2), Eq. (3), Eq. (4), Eq. (5).

### Stage 4: Score with Log-Det Aggregation

- Score via `log|K ⊗ Q|` and simplify to `N(log|K| + log|Q|)`.
- Source: Sec. III-A, Eq. (6), Eq. (7).

### Stage 5: Detect Kernel Hyperparameters (HDA)

- For vector pairs, compute candidate `G_ij = D_ij / (2(s_i^2+s_j^2))` using mean-gap and variance.
- Select `gamma_k` and `gamma_q` as minimum valid entries in `G_k`, `G_q`.
- Source: Sec. III-B, Eq. (8)-(16), Fig. 6, Fig. 8.

## Pseudocode

```text
Algorithm: RBFleX-NAS Scoring
Input: Candidate architecture f, mini-batch B={b_1...b_N}, M sampled nets for HDA
Output: score(f)

1. Detect gamma_k and gamma_q on M sampled networks:
   - For each sampled net, collect activation vectors and final-layer-input vectors.
   - Build candidate G using mean-gap and variance ratio; take min valid values.
   Source: Sec. III-B, Eq. (8)-(16), Fig. 6

2. For candidate f, run forward hooks and collect:
   - x_i: flattened activation outputs for sample i
   - y_i: flattened final-layer input map for sample i
   Source: Sec. III-A, Fig. 4, Fig. 5

3. Stack vectors into X and Y; apply column-wise normalization.
   Source: Sec. III-A, Eq. (1)

4. Compute RBF similarities:
   K_ij = exp(-gamma_k * ||x_i - x_j||^2)
   Q_ij = exp(-gamma_q * ||y_i - y_j||^2)
   Source: Sec. III-A, Eq. (2)-(5)

5. Compute score:
   score = N * (log|K| + log|Q|)
   Source: Sec. III-A, Eq. (6)-(7)

6. Rank architectures by score and select top candidates for full training.
   Source: Sec. IV-F, Sec. IV-G
```

## Training Pipeline

1. Sample candidate architectures from the benchmark/search space.
2. (Optional once per run) detect `gamma_k`, `gamma_q` with HDA.
3. For each candidate, compute RBFleX score at initialization.
4. Keep top-scored architecture(s) and evaluate final trained accuracy via benchmark API or full training.

Sources:

- Sec. III, Sec. IV, Table III.

## Inference Pipeline

1. Given a new architecture candidate, initialize model.
2. Compute score via Stage 1-4 above.
3. Insert score into candidate pool ranking.
4. Select top-k for downstream expensive validation/training.

Sources:

- Sec. III-A, Sec. IV-G.

## Complexity and Efficiency

- Time complexity: Paper reports `O(N^2.373)` for score computation step after simplification.
- Space complexity: Not explicitly provided in closed form.
- Runtime characteristics: Search-time experiments show consistently lower or competitive runtime than several training-free baselines at similar quality.
- Scaling notes: Sensitive to activation feature dimensionality; practical runs use manageable mini-batch sizes (e.g., 16).

## Implementation Notes

- Official code archives separate scripts per benchmark/task (`RBFleX_NAS-Bench-201.py`, `RBFleX_NATS-Bench-SSS.py`, `RBFleX_TransNAS_*.py`, `RBFleX_NAFBee_BERT.py`).
- Feature collection is implemented via `register_forward_hook`:
  - ReLU outputs appended into `network.K`.
  - Final module input appended into `network.Q`.
- Similarity matrix function `Simularity_Mat` computes squared distance matrix then applies `torch.exp(-gamma*dist2)`.
- Score uses `torch.linalg.slogdet`:
  - `score = batch_size_NE * (K + Q)`.
- HDA implementation (`HDA.py`) computes candidate gamma values with:
  - `M=(m1-m2)^2`,
  - `gamma_candidate = M / (2*(s1+s2))`,
  - final `gamma = min(candidate_list)`.
- Code uses float64 in key paths to reduce precision-loss in tiny-gamma settings.

## Comparison to Related Methods

- Compared with [[NASWOT]] / [[DAS]]: adds last-layer-input similarity and RBF geometry, improving low-accuracy-region separability.
- Compared with gradient-based proxies (e.g., grad norm/snip/synflow): avoids label/loss dependence while retaining competitive correlation.
- Main advantage: stronger ranking discrimination in multiple spaces and activation-search support.
- Main tradeoff: additional feature-collection overhead vs simple scalar proxies.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 4, Fig. 5, Fig. 6, Fig. 8, Fig. 9-17.
- Key table(s): Table I, Table II, Table III, Table IV, Table V.
- Key equation(s): Eq. (1)-(7), Eq. (8)-(16).
- Key algorithm(s): HDA in Sec. III-B and search analysis in Sec. IV-G.

## References

- arXiv: https://arxiv.org/abs/2503.22733
- HTML: https://arxiv.org/html/2503.22733v3
- Code: https://github.com/Edge-AI-Acceleration-Lab/RBFleX-NAS
- Local implementation: D:/PRO/essays/code_depots/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection

