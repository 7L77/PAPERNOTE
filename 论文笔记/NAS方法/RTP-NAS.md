---
title: "RTP-NAS"
type: method
source_paper: "Training-Free Robust Neural Network Search Via Pruning"
source_note: "[[RTP-NAS]]"
authors: [Qiancheng Yang, Yong Luo, Bo Du]
year: 2024
venue: ICME
tags: [nas-method, robust-nas, training-free-nas, pruning, adversarial-robustness]
created: 2026-03-25
updated: 2026-03-25
---

# RTP-NAS

## One-line Summary

> RTP-NAS uses UAP-constructed adversarial input space and pruning-time training-free metrics (adversarial NTK condition number + linear regions) to find robust architectures without adversarially training each candidate.

## Source

- Paper: [Training-Free Robust Neural Network Search Via Pruning](https://doi.org/10.1109/ICME57554.2024.10687950)
- HTML: Not provided in paper PDF
- Code: Not found in paper PDF (paper text says code will be released)
- Paper note: [[RTP-NAS]]

## Applicable Scenarios

- Problem type: robust NAS for image classification.
- Assumptions: UAP-based adversarial input space can transfer across architectures in search space.
- Data regime: supervised classification (CIFAR-10/100 in paper).
- Scale / constraints: useful when adversarially training every candidate is too expensive.
- Why it fits: scoring avoids full training loop during search and focuses on architecture-level signals.

## Not a Good Fit When

- You need guaranteed ranking quality in non-DARTS-like search spaces.
- You require immediate open-source implementation for production.
- You target robustness domains far beyond \(\ell_p\)-bounded adversarial perturbations.

## Inputs, Outputs, and Objective

- Inputs: DARTS-style candidate supernet, pre-trained source model (for UAP), training set.
- Outputs: pruned final architecture (single-path style after iterative operator pruning).
- Objective: maximize final adversarial robustness while keeping search cheap.
- Core assumptions:
  - lower adversarial NTK condition number indicates better adversarial trainability,
  - more linear regions indicate stronger expressivity in adversarial space.

## Method Breakdown

### Stage 1: Construct transferable adversarial input space

- Generate universal adversarial perturbation \(v\) with source model.
- Build \(D_A=\{(x_i+v,y_i)\}\).
- Source: Sec. 3.1, Eq. (6)-(8).

### Stage 2: Compute adversarial-space training-free metrics

- Define adversarial NTK:
  \[
  H_A(x+v, x'+v)=J(x+v)J(x'+v)^T
  \]
- Compute condition number \(\kappa_A\) of \(H_A\).
- Compute linear-region count \(R_{N,\theta}\) under adversarial inputs.
- Source: Sec. 2.1, Sec. 2.2, Sec. 3.2, Eq. (9).

### Stage 3: Rank-and-prune operators

- For each candidate operator, remove it virtually and measure:
  - \(\Delta \kappa_{A,t,o_i}\),
  - \(\Delta R_{t,o_i}\).
- Rank by descending \(\Delta\kappa_A\), ascending \(\Delta R\), then sum ranks:
  \[
  \text{Score}(o_i)=R_d(\Delta\kappa_{A,t,o_i})+R_a(\Delta R_{t,o_i})
  \]
- Prune minimum-score operator each round.
- Source: Sec. 3.2, Eq. (10)-(15), Fig. 1.

### Stage 4: Final train-and-evaluate

- Train selected architecture adversarially and evaluate with FGSM/PGD/AA.
- Source: Sec. 4.1.

## Pseudocode

```text
Algorithm: RTP-NAS
Input: search space S, training set D_S, source model C, perturbation budget epsilon
Output: robust architecture a*

1. Generate universal perturbation v using C and D_S under ||v||_p <= epsilon.
   Source: Sec. 3.1, Eq. (6)-(7)
2. Construct adversarial input space D_A = {(x_i + v, y_i)}.
   Source: Sec. 3.1, Eq. (8)
3. Initialize supernet N_0 with Kaiming initialization.
   Source: Sec. 3.2
4. For t = 0..T-1:
   4.1 For each remaining operator o_i:
       - estimate Delta kappa_A,t,o_i and Delta R_t,o_i after removing o_i
         on adversarial space D_A.
       Source: Sec. 3.2, Eq. (10)-(11)
   4.2 Compute score(o_i) = R_d(Delta kappa_A,t,o_i) + R_a(Delta R_t,o_i).
       Source: Sec. 3.2, Eq. (12)-(14)
   4.3 Prune minimum-score operator from each edge to get N_{t+1}.
       Source: Sec. 3.2, Eq. (15)
5. Stop when single-path style architecture is reached.
   Source: Sec. 3.2
6. Adversarially train searched architecture and report robust accuracy.
   Source: Sec. 4.1
```

## Training Pipeline

1. Train source model used for UAP generation.
2. Build UAP adversarial space for search-time scoring.
3. Run iterative pruning on supernet with adversarial NTK + linear-region metrics.
4. Train the final architecture with adversarial training.
5. Evaluate with FGSM, PGD20/PGD100, AutoAttack.

Sources:

- Sec. 3.1-3.2, Sec. 4.1

## Inference Pipeline

1. Use searched architecture after robust training.
2. Evaluate clean and attacked performance with standard attack suites.

Sources:

- Sec. 4.1, Table 1

## Complexity and Efficiency

- Time complexity: closed-form not reported.
- Space complexity: not reported.
- Runtime characteristics: search completes in about 1 hour (paper claim).
- Scaling notes: avoids training every candidate architecture, so search cost is significantly lower than training-based robust NAS.

## Implementation Notes

- Search space: DARTS-like cell structure.
- Initialization: Kaiming normal.
- Key pruning rule: prune ops that least hurt linear-region count while most reducing adversarial condition number.
- UAP generation:
  - depends on source architecture and epsilon budget,
  - source choice materially changes downstream robustness.
- Code availability: no explicit official URL inside the PDF.

## Comparison to Related Methods

- Compared with [[RACL]] / [[AdvRush]] / [[RNAS-CL]]:
  - RTP-NAS removes training-time robust evaluation from search loop.
- Compared with pure training-free proxies:
  - RTP-NAS explicitly builds adversarial input space before scoring.
- Main advantage: much cheaper robust search with strong attack-time accuracy.
- Main tradeoff: depends on quality/transferability of UAP construction.

## Evidence and Traceability

- Key figure(s): Fig. 1 (pipeline), Fig. 2 (searched cell visualization).
- Key table(s): Table 1 (main comparison), Table 2 (metric ablation), Table 3 (UAP ablation).
- Key equation(s): Eq. (6)-(15).
- Key algorithm(s): pruning ranking in Sec. 3.2.

## References

- DOI: https://doi.org/10.1109/ICME57554.2024.10687950
- Local PDF: D:/PRO/essays/papers/Training-Free Robust Neural Network Search Via Pruning.pdf
- Code: Not found
- Local implementation: Not archived
