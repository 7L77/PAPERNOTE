---
title: "SWAP-NAS"
type: method
source_paper: "SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS"
source_note: "[[SWAP-NAS]]"
authors: [Yameng Peng, Andy Song, Haytham M. Fayek, Vic Ciesielski, Xiaojun Chang]
year: 2024
venue: ICLR
tags: [nas-method, nas, training-free, zero-cost-proxy, swap]
created: 2026-03-14
updated: 2026-03-14
---

# SWAP-NAS

## One-line Summary
> SWAP-NAS ranks untrained candidate architectures by counting unique sample-wise ReLU activation patterns, then uses a regularized score inside evolutionary search for ultra-fast NAS.

## Source
- Paper: [SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS](https://arxiv.org/abs/2403.04161)
- HTML: https://arxiv.org/html/2403.04161
- Code: https://github.com/pym1024/SWAP
- Paper note: [[SWAP-NAS]]

## Applicable Scenarios
- Problem type: Training-free architecture ranking and fast evolutionary NAS.
- Assumptions: ReLU-based candidates can expose intermediate activations at random initialization.
- Data regime: Mostly image NAS benchmarks (CIFAR/ImageNet style settings).
- Scale / constraints: Large candidate pools where full training-per-candidate is infeasible.
- Why it fits: SWAP score gives high-resolution ranking signal with very low compute.

## Not a Good Fit When
- The search objective is strict hardware latency rather than proxy score correlation.
- Candidate models are not ReLU-centric or do not expose stable intermediate activations.
- You need a fully released SWAP-NAS search implementation out of the box.

## Inputs, Outputs, and Objective
- Inputs: Candidate architecture, mini-batch inputs, optional regularization params \(\mu,\sigma\), evolutionary search settings.
- Outputs: SWAP score (or regularized SWAP score) and selected architecture after search.
- Objective: Maximize ranking correlation with true performance under tiny search cost.
- Core assumptions: Unique sample-wise activation pattern count tracks network expressivity and final quality.

## Method Breakdown

### Stage 1: Build Activation Patterns
- Register hooks on ReLU modules and collect intermediate activations for one mini-batch.
- Binarize activations by sign and form sample-wise vectors.
- Source: Sec. 3.2, Def. 3.2; code `src/metrics/swap.py`

### Stage 2: Compute SWAP Score
- Transpose activation matrix from `(samples, neurons)` to `(neurons, samples)`.
- Count unique rows; this cardinality is \(\Psi\).
- Source: Sec. 3.2, Def. 3.3 (Eq. 4); code `SampleWiseActivationPatterns.calSWAP`

### Stage 3: Regularize for Size Control
- Compute \(f(\Theta)=\exp(-(\Theta-\mu)^2/\sigma)\) and score \(\Psi'=\Psi\cdot f(\Theta)\).
- Use \(\mu,\sigma\) to bias the search toward desired parameter range.
- Source: Sec. 3.3, Def. 3.4/3.5 (Eq. 5/6); code `cal_regular_factor`

### Stage 4: Evolutionary Search
- Initialize population, evaluate by SWAP-based score, sample candidates, crossover/mutate, insert best child, remove worst.
- Source: Algorithm 1, Appendix C

## Pseudocode
```text
Algorithm: SWAP-NAS
Input: population size P, search cycles C, sample size S, mutation budget M, regularization (mu, sigma)
Output: best architecture a*

1. Initialize population Pop with random architectures.
   Score each by SWAP or regularized SWAP.
   Source: Algorithm 1 (steps 1-6), Sec. 3.2-3.3
2. For c = 1..C:
   2.1 Randomly sample S candidates from Pop.
       Source: Algorithm 1 (step 8)
   2.2 Parent = best candidate OR crossover(best, second-best).
       Source: Algorithm 1 (step 9)
   2.3 Repeat mutation up to M times to produce children.
       Source: Algorithm 1 (steps 10-13)
   2.4 Score children with SWAP metric and keep best child.
       Source: Algorithm 1 (steps 11-14)
   2.5 Add best child to Pop and remove worst individual.
       Source: Algorithm 1 (steps 14-15)
3. Return best architecture in Pop by score.
   Source: Inference from source (selection criterion implied by algorithm text)
```

## Training Pipeline
1. Sample mini-batch inputs from target dataset.
2. For each candidate architecture: random init, compute SWAP score (repeated runs can be averaged).
3. Run evolutionary loop under compute budget.
4. Retrain searched architecture with standard supervised recipe for final report.

Sources:
- Sec. 4.1, Sec. 4.2, Algorithm 1
- `correlation.py` (metric evaluation flow)

## Inference Pipeline
1. Use searched architecture topology.
2. Train/fine-tune with target task protocol.
3. Run regular forward inference for test metrics.

Sources:
- Sec. 4.2, Table 1/2
- Inference from source

## Complexity and Efficiency
- Time complexity: Not reported as a closed-form formula.
- Space complexity: Not reported as a closed-form formula.
- Runtime characteristics: Reported search cost is ~0.004 GPU days (CIFAR-10) and ~0.006 GPU days (ImageNet).
- Scaling notes: Regularization improves correlation mainly in cell-based spaces and offers model-size control.

## Implementation Notes
- Core metric file: `src/metrics/swap.py`
- Correlation script: `correlation.py`
- Activation collection: ReLU forward hooks + concatenation of feature maps.
- Score operator: `torch.unique` on transposed sign matrix.
- Regularization: `exp(-((params-mu)^2)/sigma)` exactly matches Eq. (5).
- Important gap: Public repo mainly releases metric/correlation code; full SWAP-NAS search loop from appendix is not fully packaged as a standalone script.

## Comparison to Related Methods
- Compared with NWOT/TE-NAS/ZiCo: SWAP reports stronger and more stable cross-space correlation in the paper.
- Main advantage: Very low evaluation cost with strong ranking signal.
- Main tradeoff: Depends on activation-based proxy validity and regularization hyperparameter tuning.

## Evidence and Traceability
- Key figure(s): Fig. 3, Fig. 4, Fig. 5
- Key table(s): Table 1, Table 2, Table 3
- Key equation(s): Eq. (3), Eq. (4), Eq. (5), Eq. (6)
- Key algorithm(s): Algorithm 1

## References
- arXiv: https://arxiv.org/abs/2403.04161
- HTML: https://arxiv.org/html/2403.04161
- Code: https://github.com/pym1024/SWAP
- Local implementation: D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS

