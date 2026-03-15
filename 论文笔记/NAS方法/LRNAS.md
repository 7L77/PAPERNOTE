---
title: "LRNAS"
type: method
source_paper: "LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture"
source_note: "[[LRNAS]]"
authors: [Yuqi Feng, Zeqiong Lv, Hongyang Chen, Shangce Gao, Fengping An, Yanan Sun]
year: 2025
venue: IEEE TNNLS
tags: [nas-method, robustness, differentiable-nas, lightweight]
created: 2026-03-15
updated: 2026-03-15
---

# LRNAS

## One-line Summary
> LRNAS searches robust lightweight architectures by estimating each search primitive's joint contribution to natural accuracy and adversarial robustness with a Shapley-based estimator, then assembling primitives under a size constraint via greedy selection.

## Source
- Paper: [LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture](https://doi.org/10.1109/TNNLS.2024.3382724)
- HTML: https://doi.org/10.1109/TNNLS.2024.3382724
- Code: Not officially released in paper/public links (checked 2026-03-15)
- Paper note: [[LRNAS]]

## Applicable Scenarios
- Problem type: Robust lightweight image-classification architecture search.
- Assumptions: Primitive-level contribution at supernet stage is predictive for final architecture quality.
- Data regime: Supervised classification with adversarial training/evaluation.
- Scale / constraints: Cell-based differentiable NAS with explicit model-size threshold.
- Why it fits: Jointly optimizes robustness and accuracy while enforcing architecture compactness.

## Not a Good Fit When
- You need certified robustness guarantees rather than empirical attack robustness.
- Your search space is not cell-based and cannot be mapped to primitive contributions cleanly.
- Your compute budget cannot afford repeated permutation sampling in Shapley estimation.

## Inputs, Outputs, and Objective
- Inputs: Search space `S={o(i,j)}`, target dataset, warm-up epochs `Nw`, search epochs `Ns`, size threshold `lambda`.
- Outputs: Final architecture `A` with bounded model size.
- Objective: Maximize natural accuracy + adversarial robustness while keeping model size small.
- Core assumptions: Shapley-style marginal contributions of primitives reflect downstream architecture quality.

## Method Breakdown

### Stage 1: Supernet initialization and warm-up
- Initialize supernet weights `omega` and architecture parameters `alpha`.
- Train weights during warm-up while keeping architecture updates inactive.
- Source: Sec. III-B, Algorithm 1 (lines 1-7), Sec. IV-C.1.

### Stage 2: Shapley-based primitive valuation
- Define primitive value as average marginal gain in natural accuracy and robustness across permutations.
- Approximate with unbiased Monte Carlo estimator over sampled permutations.
- Source: Sec. III-C, Eq. (3)-(8), Theorem 1.

### Stage 3: Architecture-parameter update
- Use momentum-smoothed primitive value vector `V_i`.
- Update `alpha` with normalized `V_i` direction.
- Source: Sec. III-C, Eq. (9)-(10).

### Stage 4: Greedy architecture selection under size budget
- Keep per-edge best primitive candidate.
- Rank selected primitives by `alpha` value.
- Greedily add primitives if model size remains below threshold `lambda`.
- Source: Sec. III-D, Algorithm 2.

## Pseudocode
```text
Algorithm: LRNAS
Input: Search space S={o(i,j)}, warm-up epochs Nw, search epochs Ns, dataset D, model-size threshold lambda
Output: Robust lightweight architecture A

1. Initialize A <- empty, supernet parameters (omega, alpha) from S.
   Source: Alg. 1 lines 1-2, Sec. III-B
2. For each epoch i in [1, Nw + Ns]:
   2.1 Update omega by training on D.
       Source: Alg. 1 line 4
   2.2 If i > Nw, estimate primitive values with sampled permutations:
       Vhat_o(i,j) = (1/n) sum_t [DeltaA_o(i,j)(p_t) + DeltaR_o(i,j)(p_t)].
       Source: Eq. (3)-(8), Sec. III-C
   2.3 Momentum update primitive-value vector Vi and then update alpha.
       Source: Eq. (9)-(10)
3. Candidate extraction: for each edge, pick primitive with maximal alpha.
   Source: Eq. (2), Alg. 2 lines 2-5
4. Sort candidate primitives by alpha descending.
   Source: Alg. 2 line 6
5. Greedily add primitive into A if ModelSize(A U {primitive}) < lambda.
   Source: Alg. 2 lines 7-11
6. Return A.
   Source: Alg. 2 line 12
```

## Training Pipeline
1. Split search data into two halves (supernet train / validation).
2. Run 60 search epochs with 15 warm-up epochs.
3. During search, use FGSM (epsilon=8/255) to evaluate robustness signal for primitive valuation.
4. After architecture derivation, adversarially train final architecture (e.g., 7-step PGD for CIFAR).

Sources:
- Sec. IV-C.1, Sec. IV-C.2, Sec. V-A.

## Inference Pipeline
1. Use the selected architecture `A` as a normal classifier backbone.
2. Perform standard forward inference on clean inputs.
3. Robustness evaluation uses FGSM/PGD/C&W protocols as in paper benchmarks.

Sources:
- Sec. IV-C.2, Sec. V-A.

## Complexity and Efficiency
- Time complexity (search valuation + selection): `O(n * |O| * |E|)`.
- Selection complexity: `O(|O| * |E|)`.
- Reported search cost: about `0.4 GPU days` in CIFAR experiments.

## Implementation Notes
- Warm-up stabilizes architecture-parameter updates before value-driven search.
- `lambda` controls robustness/accuracy/size tradeoff; paper picks `2.0M` as best overall setting on CIFAR-10.
- Greedy selection contributes strongly to parameter reduction and robustness gains in ablations.
- The method is tied to primitive-level representation in differentiable NAS search spaces.
- Official code repository was not explicitly provided in accessible paper links.

## Comparison to Related Methods
- Compared with [[DARTS]]: LRNAS injects robustness-aware primitive valuation instead of only differentiable score optimization.
- Compared with [[E2RNAS]] / robust NAS peers: LRNAS adds explicit primitive contribution accounting and size-constrained greedy assembly.
- Main advantage: Better robustness-size tradeoff and strong transfer to larger datasets.
- Main tradeoff: More expensive than the cheapest differentiable baselines due to permutation sampling.

## Evidence and Traceability
- Key figure(s): Fig. 2-7.
- Key table(s): Table I-IX.
- Key equation(s): Eq. (2)-(10).
- Key algorithm(s): Algorithm 1 and Algorithm 2.

## References
- DOI: https://doi.org/10.1109/TNNLS.2024.3382724
- HTML: https://doi.org/10.1109/TNNLS.2024.3382724
- Code: Not officially released (as of 2026-03-15)
- Local implementation: Not archived
