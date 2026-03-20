---
title: "UP-NAS"
type: method
source_paper: "UP-NAS: Unified Proxy for Neural Architecture Search"
source_note: "[[UP-NAS]]"
authors: [Yi-Cheng Huang, Wei-Hua Li, Chih-Han Tsou, Jun-Cheng Chen, Chu-Song Chen]
year: 2024
venue: "CVPR Workshops"
tags: [nas-method, nas, training-free, zero-cost-proxy, predictor-based-nas, gradient-ascent]
created: 2026-03-20
updated: 2026-03-20
---

# UP-NAS

## One-line Summary
> UP-NAS learns a weighted multi-proxy objective over zero-cost signals, predicts those signals from architecture latents with MPE, and then performs latent-space gradient ascent to search architectures quickly.

## Source
- Paper: [UP-NAS: Unified Proxy for Neural Architecture Search](D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf)
- HTML: Not provided in paper
- Code: https://github.com/AI-Application-and-Integration-Lab/UP-NAS
- Paper note: [[UP-NAS]]

## Applicable Scenarios
- Problem type: Training-free or low-cost NAS in cell-based search spaces where multiple zero-cost proxies are available.
- Assumptions: A smooth latent representation of architectures exists, and a weighted proxy sum has stable enough transfer across datasets/search spaces.
- Data regime: Requires proxy scores for many sampled architectures, plus a small benchmark subset for learning proxy weights.
- Scale / constraints: Especially useful when repeated proxy evaluation is expensive but a predictor can amortize that cost.
- Why it fits: It converts multi-proxy architecture scoring into a differentiable latent optimization problem instead of repeated discrete search.

## Not a Good Fit When
- The search space lacks a reliable encoder-decoder pair for continuous architecture embeddings.
- Proxy behavior changes drastically across domains, making fixed learned weights unstable.
- You need code-level reproducibility today; the archived official repo still has no released implementation.

## Inputs, Outputs, and Objective
- Inputs: Architecture `A`, proxy vector `[f^1_zc(A), ..., f^M_zc(A)]`, learned encoder/decoder, and proxy weights `lambda`.
- Outputs: Searched architecture `A*` and its predicted unified proxy score.
- Objective: Maximize the unified proxy `UP(A)=sum_i lambda_i f^i_zc(A)` using a learned surrogate over latent architecture embeddings.
- Core assumptions: Proxy fusion improves ranking, and latent gradient steps correspond to meaningful architecture improvements after decoding.

## Method Breakdown
### Stage 1: Learn architecture embedding space
- Represent each cell architecture as DAG adjacency matrix plus operation matrix.
- Use a [[Variational Graph Autoencoder]] with [[Graph Isomorphism Network]] encoders to map architectures to continuous latent vectors and decode them back.
- Source: Sec. 3.2, Eq. (2), Fig. 3.

### Stage 2: Train Multi-Proxy Estimator (MPE)
- Freeze or reuse the pretrained architecture encoder.
- Feed architecture embeddings into a two-hidden-layer MLP to predict all proxy scores jointly.
- Train with MSE against the actual proxy vector.
- Source: Sec. 3.3, Eq. (3)-(4), Fig. 2.

### Stage 3: Learn unified proxy weights
- Search proxy weights `lambda` on a small NAS-Bench-201-CIFAR-10 subset.
- Use [[Tree-structured Parzen Estimator]] to maximize [[Kendall's Tau]] between weighted proxy score and ground-truth validation accuracy.
- Reuse the resulting weights on unseen spaces/datasets.
- Source: Sec. 3.4-3.5, Eq. (1), Table 1.

### Stage 4: Search by latent gradient ascent
- Sample an initial architecture and encode it to `Z`.
- Freeze encoder + MLP + proxy weights, define `F(Z)=sum_i lambda_i f_MLP(Z;W)_i`.
- Update `Z <- Z + eta * grad_Z F(Z)` for several steps.
- Decode the final latent vector back into a discrete architecture.
- Source: Sec. 3.4, Eq. (5)-(6), Fig. 2.

## Pseudocode
```text
Algorithm: UP-NAS
Input: Search space S, proxy set {f^i_zc}_{i=1..M}, architecture autoencoder Enc/Dec, sampled architectures for MPE training
Output: Best architecture A*

1. Pretrain architecture autoencoder on architectures from S.
   Source: Sec. 3.2 / Eq. (2) / Fig. 3
2. Compute proxy vectors for sampled architectures and encode them to latent embeddings.
   Source: Sec. 3.3 / Sec. 3.5
3. Train MPE to regress all M proxy scores from the embedding.
   Source: Eq. (3)-(4)
4. Search proxy weights lambda with TPE to maximize Kendall's tau on a small benchmark subset.
   Source: Sec. 3.4-3.5 / Table 1
5. Sample an initial architecture A0 and encode it as Z0.
   Source: Sec. 3.4
6. Repeat gradient ascent on F(Z)=sum_i lambda_i f_MLP(Z;W)_i.
   Source: Eq. (5)-(6)
7. Decode the optimized latent ZT into a discrete architecture A*.
   Source: Sec. 3.4 / Fig. 3
8. Fully train/evaluate A* under the benchmark protocol.
   Source: Experimental protocol in Sec. 4
```

## Training Pipeline
1. Pretrain the architecture autoencoder on cell graphs.
2. Compute or load zero-cost proxy scores for sampled architectures.
3. Train MPE on embedding-to-proxy regression.
4. Search a global proxy weight vector `lambda` with TPE on NAS-Bench-201-CIFAR-10.
5. Freeze the trained components before search.

Sources:
- Sec. 3.2-3.5, Table 1.

## Inference Pipeline
1. Sample an architecture from the target search space.
2. Encode it to latent vector `Z`.
3. Perform gradient ascent on the frozen unified-proxy objective.
4. Decode the optimized latent into a discrete architecture.
5. Train the found architecture with the standard benchmark recipe and use it as the final model.

Sources:
- Sec. 3.4, Fig. 2, Sec. 4.

## Complexity and Efficiency
- Time complexity: Dominated by one-time proxy computation for sampled architectures, MPE training, and latent optimization.
- Space complexity: Depends on proxy cache size plus autoencoder/MPE parameters.
- Runtime characteristics:
  - `grasp` takes about `10 sec` per DARTS architecture.
  - each of the other 12 proxies is about `1 sec`.
  - MPE training on NAS-Bench-201 and DARTS takes less than `2 minutes`.
  - DARTS latent search is reported at around `5 sec`.
- Scaling notes: The more search steps you would otherwise spend recomputing proxies, the larger the payoff from MPE amortization.

## Implementation Notes
- Search space encoding:
  - adjacency matrix `A` plus one-hot operation matrix `X`
  - augmented adjacency `A + A^T`
- Decoder details:
  - adjacency reconstruction via `sigmoid(z_i^T z_j)`
  - operation reconstruction via `softmax(W_o Z + b_o)`
- Latent dimensions:
  - NAS-Bench-201: `128`
  - DARTS: `352`
- MPE:
  - two hidden layers
  - linear + batch norm + ReLU blocks
  - supervised by proxy vector MSE, not accuracy regression
- Proxy choices:
  - `snip`, `flops`, `params`, `l2 norm`, `grasp`, `gradnorm`, `synflow`, `jacov`, `EPENAS`, `Zen`, `fisher`, `plain`, `Nwot`
- Learned weighting behavior:
  - strongest positive weights: `jacov`, `synflow`, `flops`
  - negative weights: `params`, `fisher`, `snip`, `l2 norm`
  - selected mode keeps `flops`, `synflow`, `jacov`, `Nwot`
- Reproducibility caveat:
  - local archived repo `D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search`
  - remote is official, but archived commit `2601145` contains only `README.md` and `LICENSE`
  - this note is therefore paper-derived rather than code-verified

## Comparison to Related Methods
- Compared with [[NAO]]: both search in continuous architecture space, but UP-NAS optimizes a unified proxy rather than a direct performance predictor.
- Compared with [[ProxyBO]]: both combine multiple proxies, but UP-NAS uses fixed learned weights plus latent gradient ascent instead of Bayesian optimization over candidate architectures.
- Main advantage: Fast search after amortized proxy learning, with a clear bridge from multi-proxy fusion to differentiable search.
- Main tradeoff: Success depends on latent smoothness and on the transferability of a single global proxy weight vector.

## Evidence and Traceability
- Key figure(s): Fig. 1 (MPE + unified proxy idea), Fig. 2 (train/search pipeline), Fig. 3 (autoencoder), Fig. 4-5 (searched DARTS cells).
- Key table(s): Table 1 (proxy weights), Table 2 (rank correlation), Table 3-4 (NAS-Bench-201 performance), Table 5 (DARTS/ImageNet), Table 6 (search ablation), Table 7 (MLP ablation).
- Key equation(s): Eq. (1) unified proxy, Eq. (2) VGAE objective, Eq. (3)-(4) MPE loss, Eq. (5)-(6) gradient ascent.
- Key algorithm(s): No explicit algorithm block; the search procedure is specified by Eq. (5)-(6) and Fig. 2.

## References
- Paper PDF: D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf
- Code URL: https://github.com/AI-Application-and-Integration-Lab/UP-NAS
- Local implementation: D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search
