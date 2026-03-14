---
title: "WRCor"
type: method
source_paper: "Zero-Shot Neural Architecture Search with Weighted Response Correlation"
source_note: "[[WRCor]]"
authors: [Kun Jing, Luoyu Chen, Jungang Xu, Jianwei Tai, Yiyu Wang, Shuaimin Li]
year: 2025
venue: arXiv
tags: [nas-method, zero-shot-nas, training-free-proxy, response-correlation]
created: 2026-03-14
updated: 2026-03-14
---

# WRCor

## One-line Summary

> WRCor estimates architecture quality without training by computing log-det of layer-weighted activation/gradient response-correlation matrices, then uses this proxy in random/RL/evolution NAS search loops.

## Source

- Paper: [Zero-Shot Neural Architecture Search with Weighted Response Correlation](https://arxiv.org/abs/2507.08841)
- HTML: https://arxiv.org/html/2507.08841v2
- Code: https://github.com/kunjing96/ZSNAS-WRCor
- Paper note: [[WRCor]]

## Applicable Scenarios

- Problem type: Zero-shot ranking of candidate neural architectures for image classification.
- Assumptions: Cross-sample response correlation at initialization is informative for final architecture quality.
- Data regime: Can use dataset minibatches; can also run on random noise with some degradation.
- Scale / constraints: Useful when many candidates must be screened under tight compute budgets.
- Why it fits: It avoids full training and provides a unified scalar score combining expressivity and generalizability signals.

## Not a Good Fit When

- You need calibrated final accuracy prediction instead of relative ranking.
- Search space is very large and proxy correlation already degrades severely (e.g., NB101 trend in paper).
- Architectures or activations break stable response-correlation computation.

## Inputs, Outputs, and Objective

- Inputs: Candidate architecture \(f\), initialized weights, minibatch inputs \(X\), loss function for backward pass.
- Outputs: ACor, RCor, WRCor scores; optional voting scores SPW/SJW.
- Objective: Rank architectures so high-performing ones appear earlier in search.
- Core assumptions: Better architectures yield lower off-diagonal response correlation and thus larger log-det scores after aggregation.

## Method Breakdown

### Stage 1: Collect Response Tensors

- Run forward pass and collect pre-activation activations per layer/unit.
- Run backward pass and collect gradients w.r.t hidden feature maps.
- Source: Sec. 3.1, Sec. 3.2, Sec. 3.3

### Stage 2: Build Correlation Matrices

- For each response set across samples, compute correlation-coefficient matrix.
- Take absolute values and aggregate over units.
- Source: Sec. 3.3.1, Eq. (1), Eq. (8), Eq. (9)

### Stage 3: Layer-wise Weighting (WRCor)

- Apply exponentially increasing weights from bottom to top layers.
- Aggregate activation and gradient correlation matrices into one matrix \(K\).
- Source: Sec. 3.3.2, Eq. (10), Eq. (11)

### Stage 4: Scalar Proxy Mapping

- Compute proxy score by \( \log(\det(K)) \) (implemented via `slogdet`).
- Higher score indicates better architecture in their framework.
- Source: Sec. 3.3.1, Eq. (6)-(8), code `act_grad_cor_weighted.py`

### Stage 5: Search with Proxy

- Use proxy as architecture estimator inside random search, RL, or regularized evolution.
- Optionally use majority voting proxy SJW/SPW.
- Source: Sec. 3.4, Alg. 1, Alg. 2, Sec. 4.3

## Pseudocode

```text
Algorithm: WRCor-based Zero-shot NAS
Input: Search space S, budget N, minibatch X, proxy set M
Output: Best architecture a*

1. Sample architecture a from S (random / RL controller / evolution mutation).
   Source: Sec. 3.4, Alg. 1-2
2. Initialize a and run one forward pass on X; collect pre-activation responses.
   Source: Sec. 3.1, Sec. 3.3
3. Run backward pass; collect gradient responses per layer.
   Source: Sec. 3.2, Sec. 3.3
4. For each layer l and response unit i, compute correlation matrix C_{l,i} over samples.
   Source: Sec. 3.3.1, Eq. (1), Eq. (9)
5. Aggregate K = sum_l sum_i 2^l * (|C^A_{l,i}| + |C^G_{l,i}|).
   Source: Sec. 3.3.2, Eq. (11)
6. Score(a) = log(det(K)).
   Source: Eq. (10), code `slogdet`
7. Optionally combine with SynFlow/JacCor or SynFlow/PNorm via majority voting.
   Source: Sec. 3.3.3
8. Update search state and keep best architecture under budget N.
   Source: Sec. 3.4, Alg. 1-2
```

## Training Pipeline

1. No architecture-specific full training is needed for proxy scoring.
2. For each candidate, run lightweight forward/backward only to compute responses.
3. Use proxy score in search loop to select candidate architectures.
4. Train only final selected architecture(s) for true evaluation.

Sources:

- Sec. 1, Sec. 3, Sec. 4.1.4-4.1.5

## Inference Pipeline

1. Given a candidate architecture, initialize weights.
2. Compute WRCor score from one minibatch.
3. Rank candidates by score (or voting score).
4. Select top architectures for downstream training/deployment.

Sources:

- Sec. 3.3, Sec. 3.4, Sec. 4.3

## Complexity and Efficiency

- Time complexity: Not reported as closed-form.
- Space complexity: Not reported as closed-form.
- Runtime characteristics: Paper reports about 2 seconds per architecture for WRCor estimation (NB201 context) and 0.17 GPU day search for RE-SJW in MobileNetV2.
- Scaling notes: Performance drops when moving to larger search space (NB101 vs NB201), motivating voting and better proxies.

## Implementation Notes

- Code path for weighted proxy: `foresight/pruners/measures/act_grad_cor_weighted.py`.
- Uses hooks on ReLU modules to gather activations and gradients, then computes `np.corrcoef`.
- Applies layer weight `2**i` and accumulates into `net.K`.
- Uses `np.linalg.slogdet(net.K)` for log-determinant stability.
- Non-weighted baseline RCor in `act_grad_cor.py`.
- Search integration in `search.py`:
  - `Random_NAS`, `RL_NAS`, `Evolved_NAS`
  - Typical measure config in README: `+act_grad_cor_weighted +synflow +jacob_cor`.

## Comparison to Related Methods

- Compared with NASWOT/JacCor-style expressivity proxies: WRCor adds gradient-side signal and layer weighting.
- Compared with ZiCo: WRCor is competitive or better on NB201 proxy correlation, while remaining simple to integrate.
- Main advantage: Unified proxy form with good empirical robustness across datasets/batch/initialization.
- Main tradeoff: Still not universally dominant in larger search spaces; voting is often needed.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2
- Key table(s): Table 2, Table 3, Table 4, Table 7, Table 8, Table 9, Table 10
- Key equation(s): Eq. (1), Eq. (8), Eq. (9), Eq. (10), Eq. (11)
- Key algorithm(s): Alg. 1 (RL), Alg. 2 (Regularized Evolution)

## References

- arXiv: https://arxiv.org/abs/2507.08841
- HTML: https://arxiv.org/html/2507.08841v2
- Code: https://github.com/kunjing96/ZSNAS-WRCor
- Local implementation: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation


