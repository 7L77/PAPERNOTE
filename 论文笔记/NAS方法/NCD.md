---
title: "NCD"
type: method
source_paper: "Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS"
source_note: "[[NCD]]"
authors: [Haidong Kang, Lianbo Ma, Pengjun Chen, Guo Yu, Xingwei Wang, Min Huang]
year: 2025
venue: ICCV
tags: [nas-method, training-free-nas, activation-based-proxy, ncd]
created: 2026-03-14
updated: 2026-03-14
---

# NCD

## One-line Summary
> NCD patches activation-based zero-cost proxies (e.g., NWOT/SWAP) with stochastic masking and non-linear rescaling so their ranking correlation stays positive in deep search subspaces.

## Source
- Paper: [Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS](https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html)
- PDF: https://openaccess.thecvf.com/content/ICCV2025/papers/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.pdf
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf
- Code: Not found (ICCV page + supplementary checked on 2026-03-14)
- Paper note: [[NCD]]

## Applicable Scenarios
- Problem type: Training-free architecture ranking/search with activation-based proxies.
- Assumptions: Negative correlation appears as architecture non-linearity/depth grows.
- Data regime: Image-classification NAS search spaces (NB-201/101, DARTS, MobileNet-like, etc.).
- Scale / constraints: Suitable when per-candidate full training is infeasible and ranking quality is the bottleneck.
- Why it fits: NCD directly modifies proxy scoring dynamics rather than replacing the search framework.

## Not a Good Fit When
- The pipeline does not use activation-based proxy scores.
- You cannot tune/validate mask ratio `alpha` for the target search space.
- You need a fully released official codebase for immediate deployment.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture, mini-batch inputs, baseline AZP scorer (e.g., NWOT/SWAP), mask ratio `alpha`.
- Outputs: NCD-adjusted proxy score (`NCD-NWOT` or `NCD-SWAP`) and ranked candidates.
- Objective: Recover/boost rank correlation with true validation accuracy under zero/low training cost.
- Core assumptions: Non-linearity accumulation is the main cause of correlation collapse in deep subspaces.

## Method Breakdown

### Stage 1: Diagnose Negative Correlation
- Partition search space by convolution count and compare Spearman correlation between AZP score and real accuracy.
- Source: Sec. 3.1, Fig. 2, Table 1.

### Stage 2: Stochastic Activation Masking (SAM)
- In convolution scoring path, apply Bernoulli mask to activation values:
  \( y=\sum(W\odot M\odot X),\ M\sim Bernoulli(1-\alpha)\).
- Reduces activation-summation burden and mitigates over-amplified non-linearity.
- Source: Sec. 4.1, Eq. (4), supplementary Alg. 1 (lines 4-6).

### Stage 3: Non-linear Rescaling (NIR)
- Analyze BN/LN aggregation behavior (Theorem 4.1/4.2) and use LN-style normalization in proxy evaluation to stabilize non-linearity.
- Source: Sec. 4.2, Eq. (5)-(10), Theorem 4.1/4.2, supplementary Alg. 1 (lines 7-8).

### Stage 4: Plug into Existing AZP
- Replace raw AZP evaluation with NCD-evaluation and produce `NCD-SWAP` / `NCD-NWOT`.
- Source: Sec. 4, Sec. 5, Fig. 5, Table 2/3.

## Pseudocode
```text
Algorithm: NCD-Enhanced AZP Evaluation
Input: architecture a, input mini-batch X, baseline AZP metric f_azp, mask ratio alpha
Output: NCD-adjusted proxy score s

1. Initialize a and construct feature tensors through forward path.
   Source: Sec. 2.1, Sec. 4
2. For each convolutional operation in scoring path:
   sample Bernoulli mask M with prob(keep)=1-alpha and apply masked activation.
   Source: Sec. 4.1, Eq. (4), Supp. Alg. 1 lines 4-6
3. Apply non-linear rescaling / normalization handling (LN-based in AZP evaluation path).
   Source: Sec. 4.2, Theorem 4.2, Supp. Alg. 1 lines 7-8
4. Compute AZP score on transformed activations:
   s = f_azp(transformed_features).
   Source: Sec. 4, Fig. 5
5. Rank architectures by s and run the outer search loop (e.g., evolutionary sampler).
   Source: Sec. 5 experiments, Supp. Alg. 1 (framework-level flow)
```

## Training Pipeline
1. Sample candidate architectures from target search space.
2. Score each candidate using NCD-adjusted AZP at initialization.
3. Keep top-ranked candidates in outer search loop.
4. Retrain selected architecture(s) with standard protocol for final accuracy.

Sources:
- Sec. 5, Table 2, Table 3, supplementary App. B.

## Inference Pipeline
1. Given a candidate architecture, run one NCD-adjusted proxy evaluation.
2. Convert score to ranking among current candidate pool.
3. Output top architectures for downstream full training/deployment.

Sources:
- Sec. 4, Sec. 5, Fig. 1/2/5.

## Complexity and Efficiency
- Time complexity: Not reported as a closed-form equation.
- Space complexity: Not reported as a closed-form equation.
- Runtime characteristics: NB-101 reports 29.01 ms/arch for NCD-NWOT; DARTS setting reports search cost down to 0.002 GPU-days.
- Scaling notes: Gains are larger in deeper subspaces where baseline AZP correlation becomes negative.

## Implementation Notes
- Hyperparameter: `alpha` controls masking density (paper ablation uses multiple values; NB-201 best around 0.95 in reported setup).
- SAM and NIR are both effective individually, strongest jointly (Table 7).
- The method is designed as a wrapper around existing AZPs, not a brand-new search algorithm.
- Practical workflow: first verify correlation on your subspaces, then tune `alpha` in a small sweep.
- Code status in this workspace: no official repository link identified from paper/supplementary as of 2026-03-14.

## Comparison to Related Methods
- Compared with [[Zero-Cost Proxy]] baselines (NWOT/SWAP): directly addresses sign-flip correlation failure in deep subspaces.
- Compared with [[AZ-NAS]]: focuses on fixing activation-based proxy pathology rather than proxy fusion.
- Main advantage: minimal modification, strong correlation recovery when baseline AZP collapses.
- Main tradeoff: still depends on proxy validity assumptions and alpha calibration.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 4, Fig. 5.
- Key table(s): Table 1, Table 2, Table 3, Table 7, Table 8.
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5)-(10).
- Key algorithm(s): Algorithm 1 in supplementary material.

## References
- Paper page: https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html
- PDF: https://openaccess.thecvf.com/content/ICCV2025/papers/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.pdf
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf
- Code: Not found
- Local implementation: Not archived
