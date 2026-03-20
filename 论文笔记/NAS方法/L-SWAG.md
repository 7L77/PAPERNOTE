---
title: "L-SWAG"
type: method
source_paper: "L-SWAG: Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers"
source_note: "[[L-SWAG]]"
authors: [Sofia Casarin, Sergio Escalera, Oswald Lanz]
year: 2025
venue: CVPR
tags: [nas-method, nas, zero-cost-proxy, training-free, vision-transformer]
created: 2026-03-20
updated: 2026-03-20
---

# L-SWAG

## One-line Summary
> L-SWAG ranks untrained architectures by multiplying layer-selected gradient-variance statistics with layer-wise activation-pattern expressivity, and LIBRA further improves ranking by benchmark-specific proxy triad selection.

## Source
- Paper: [L-SWAG (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/papers/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.pdf)
- HTML: https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html
- Code: Not found on paper page/supplementary page at note time
- Paper note: [[L-SWAG]]

## Applicable Scenarios
- Problem type: Training-free architecture ranking and search in CNN/ViT spaces.
- Assumptions: Gradient variance and activation pattern diversity are informative at initialization.
- Data regime: No architecture training for proxy scoring; benchmark meta-statistics needed for LIBRA calibration.
- Scale / constraints: Large search spaces where full training is unaffordable.
- Why it fits: Keeps zero-shot evaluation cheap while improving robustness across heterogeneous benchmarks.

## Not a Good Fit When
- You cannot compute backward gradients at all (L-SWAG needs gradient statistics).
- Search space has no reliable benchmark meta-distribution for LIBRA-style proxy calibration.
- You require end-to-end reproducibility from official released code only.

## Inputs, Outputs, and Objective
- Inputs: Randomly initialized architecture `N`, mini-batch `(X, y)`, selected layer interval `[l_hat, L_hat]`, and optional proxy pool for LIBRA.
- Outputs: Proxy score for ranking (`L-SWAG`), or ensemble proxy set `{z1,z2,z3}` under LIBRA.
- Objective: Maximize rank consistency between proxy scores and validation accuracy ranking.
- Core assumptions: Layer importance is non-uniform; combining trainability and expressivity improves transferability.

## Method Breakdown
### Stage 1: Layer-wise gradient statistics for trainability
- Compute gradient absolute values per layer and aggregate variance-based term over selected layers.
- Source: Sec. 3.1, Eq. (1), Eq. (5), Fig. 2.

### Stage 2: Layer-wise sample-wise activation patterns for expressivity
- Build per-layer binary activation pattern sets and use their cardinality as expressivity score.
- Source: Sec. 3.1, Def. 1, Def. 2, Eq. (7), Eq. (8).

### Stage 3: Multiplicative proxy synthesis
- Multiply trainability and expressivity terms into final `L-SWAG`.
- Source: Sec. 3.1, Eq. (1).

### Stage 4: LIBRA proxy triad selection (optional for search)
- Select `z1` by highest correlation, `z2` by minimum IG among strong candidates, `z3` by bias matching.
- Source: Sec. 3.2, Alg. 1, Eq. (9).

## Pseudocode
```text
Algorithm: L-SWAG + LIBRA
Input: Architecture N, init weights theta, batch (X,y), proxy set Z with benchmark correlations
Output: Architecture ranking score s (or ensemble score)

1. Determine informative layer interval [l_hat, L_hat] from percentile spikes on gradient statistics.
   Source: Sec. 3.1, Fig. 2, Eq. (6)
2. Compute trainability term Lambda over selected layers using gradient variance aggregation.
   Source: Sec. 3.1, Eq. (1), Eq. (5)
3. Compute expressivity term Psi as cardinality of layer-wise sample-wise activation patterns.
   Source: Sec. 3.1, Def. 1-2, Eq. (7-8)
4. Set s = Lambda * Psi and rank architectures by descending s.
   Source: Sec. 3.1, Eq. (1)
5. (Optional LIBRA) choose z1=best-correlation proxy, z2=min-IG proxy, z3=bias-matched proxy, then merge for search.
   Source: Sec. 3.2, Alg. 1, Eq. (9)
```

## Training Pipeline
1. No architecture training is needed for L-SWAG scoring itself.
2. Run one/few forward-backward passes on sampled architectures to collect gradients and activations.
3. Calibrate layer interval based on benchmark-wise gradient percentile analysis.
4. For LIBRA, precompute proxy correlations and bias statistics on benchmark candidates.

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4 (Experimental Settings).

## Inference Pipeline
1. For each candidate architecture, compute L-SWAG score at initialization.
2. Rank candidates and select top-k for downstream NAS steps.
3. If using LIBRA, compute/compose selected proxy triad scores and rerank.

Sources:
- Sec. 4.1, Sec. 4.2, Tab. 1, Tab. 2.

## Complexity and Efficiency
- Time complexity: Dominated by gradient/activation extraction on candidate batch.
- Space complexity: Activation and gradient tensors for selected layers; reported memory around 10 GB for 1000 ViTs at 224x224.
- Runtime characteristics: Reported ~31 min for gradient stats on 1000 ViTs, then ~4 min for L-SWAG scoring after layer selection.
- Scaling notes: Reported stable gains across NB101/NB301/TransNAS/AutoFormer, with stronger robustness than many single proxies.

## Implementation Notes
- Layer selection is a key performance lever; all-layers aggregation is consistently weaker in ablation.
- Removing gradient mean term `mu` improves robustness on multiple benchmarks in reported ablations.
- Expressivity term is crucial for ViT performance; gradient-only variants underperform more often.
- LIBRA uses a practical window (`rho_best - 0.1 < rho <= rho_best`) before IG/bias filtering.
- Official code for this paper is not explicitly released; implementation details are paper-derived.

## Comparison to Related Methods
- Compared with [[ZiCo-BC]]: L-SWAG removes mean-gradient dependency and adds layer-wise expressivity coupling.
- Compared with [[SWAP-NAS]]: L-SWAG keeps SWAP-like expressivity but adds gradient trainability and layer interval selection.
- Main advantage: Better cross-benchmark ranking consistency, especially including ViT space.
- Main tradeoff: Requires both gradient and activation extraction plus benchmark-specific calibration for best results.

## Evidence and Traceability
- Key figure(s): Fig. 1 (framework), Fig. 2 (layer-selection motivation), Fig. 3/4 (correlation comparisons).
- Key table(s): Tab. 1 (ensemble comparison), Tab. 2 (search outcomes), Tab. 3 (L-SWAG ablation), Tab. 4 (LIBRA ablation).
- Key equation(s): Eq. (1), Eq. (5), Eq. (7), Eq. (8), Eq. (9).
- Key algorithm(s): Algorithm 1 (LIBRA).

## References
- arXiv: Not provided in accessed source
- HTML: https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html
- Code: Not found on paper page/supplementary page at note time
- Local implementation: Not archived
