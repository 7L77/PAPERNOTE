---
title: "CRoZe"
type: method
source_paper: "Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations"
source_note: "[[CRoZe]]"
authors: [Hyeonjeong Ha, Minseon Kim, Sung Ju Hwang]
year: 2023
venue: NeurIPS
tags: [nas-method, robust-nas, zero-cost-proxy, training-free]
created: 2026-03-15
updated: 2026-03-15
---

# CRoZe

## One-line Summary

> CRoZe estimates robust NAS quality at initialization by multiplying feature/parameter/gradient consistency between clean and perturbed surrogate networks after one-step updates.

## Source

- Paper: [Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations](https://arxiv.org/abs/2306.05031)
- HTML: https://arxiv.org/html/2306.05031
- Code: https://github.com/HyeonjeongHa/CRoZe
- Paper note: [[CRoZe]]

## Applicable Scenarios

- Problem type: Robust architecture ranking/search under diverse perturbations.
- Assumptions: One-step surrogate behavior is rank-consistent with final robust accuracy.
- Data regime: Supervised image classification (CIFAR/ImageNet16-120 in paper).
- Scale / constraints: When full adversarial supernet training is too expensive.
- Why it fits: Proxy evaluation avoids iterative architecture training and still reflects robust ranking.

## Not a Good Fit When

- You require certified robustness guarantees instead of empirical robustness ranking.
- Perturbation family is far outside semantic-preserving image perturbations.
- Task domain has weak alignment between single-step gradients and final optimization trajectory.

## Inputs, Outputs, and Objective

- Inputs: Architecture `A`, minibatch `(x, y)`, perturbed input `x'`, clean net `f_theta`, robust net `f_theta^r`.
- Outputs: Scalar proxy score `CRoZe(A)`.
- Objective: Rank architectures by expected final clean+robust performance.
- Core assumptions: Better architectures align features, parameter updates, and gradients across clean/perturbed tasks.

## Method Breakdown

### Stage 1: Build surrogate robust branch

- Start from randomly initialized clean model `f_theta`.
- Create robust surrogate by layer-wise parameter perturbation to maximize loss (Eq. 3).
- Generate input perturbation with FGSM on robust surrogate (Eq. 4).
- Source: Sec. 3.2, Eq. (3)(4), Fig. 1(b)

### Stage 2: Compute feature consistency

- Forward clean input through `f_theta` and perturbed input through `f_theta^r`.
- Compute layer-wise cosine similarity `Z_m` (Eq. 5).
- Source: Sec. 3.3, Eq. (5)

### Stage 3: Compute parameter and gradient consistency

- Compute clean/robust gradients `g, g^r` (Eq. 6).
- Apply one-step updates to get `theta_1, theta_1^r` (Eq. 7).
- Compute parameter similarity `P_m` (Eq. 8) and gradient alignment `G_m` (Eq. 9).
- Source: Sec. 3.3, Eq. (6)(7)(8)(9)

### Stage 4: Aggregate proxy score

- Multiply three consistencies and sum across layers:
  `CRoZe = sum_m Z_m * P_m * G_m`.
- Source: Eq. (10), Table 1/2/3 evidence

## Pseudocode

```text
Algorithm: CRoZe
Input: architecture A, minibatch (x, y), perturbation budget epsilon
Output: scalar robustness proxy s

1. Initialize clean surrogate f_theta from architecture A.
   Source: Sec. 3.2
2. Construct robust surrogate f_theta^r by layer-wise parameter perturbation maximizing CE loss.
   Source: Eq. (3), Sec. 3.2
3. Generate perturbed batch x' via FGSM on f_theta^r.
   Source: Eq. (4), Sec. 3.2
4. Forward clean branch (x -> f_theta) and robust branch (x' -> f_theta^r), collect layer features.
   Source: Eq. (5), Sec. 3.3
5. Compute gradients g, g^r and one-step updated params theta_1, theta_1^r.
   Source: Eq. (6)(7), Sec. 3.3
6. For each layer m, compute Z_m, P_m, G_m and accumulate s += Z_m * P_m * G_m.
   Source: Eq. (5)(8)(9)(10)
7. Return s as architecture robustness score.
   Source: Eq. (10)
```

## Training Pipeline

1. Sample candidate architectures in search space (random/mutate/warmup+move).
2. For each candidate, compute CRoZe score from one minibatch.
3. Select top-ranked architecture(s).
4. Train selected architecture with standard training or adversarial training for final evaluation.

Sources:

- Sec. 4.2, 4.3
- `main.py` (`sample_arch`)
- `sampling.py`

## Inference Pipeline

1. Use architecture selected by CRoZe.
2. Load trained checkpoint.
3. Evaluate on clean set and perturbation suites (FGSM/PGD/CW/DeepFool/SPSA/LGV/AA + corruptions).

Sources:

- Sec. 4
- Source: Inference from source

## Complexity and Efficiency

- Time complexity: Not given in closed form; dominated by proxy eval + sampling count.
- Space complexity: Two surrogate networks plus intermediate feature/gradient buffers.
- Runtime characteristics:
  - DARTS/CIFAR-10 search time reported at about 17,066 GPU sec.
  - Robust one-shot baselines are much slower (e.g., 251,245~274,062 GPU sec).
- Scaling notes: Runtime grows mostly with number of sampled architectures, not with full training epochs.

## Implementation Notes

- Local code path: `D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations`
- Core proxy implementation:
  - `zero_cost_methods/pruners/measures/croze.py`
  - `zero_cost_methods/pruners/p_utils.py`
- `adj_weights(...)` performs one-step gradient-based weight perturbation for robust surrogate construction.
- `fgsm_attack(...)` in `croze.py` creates perturbed inputs used for the robust branch.
- Layer-wise metrics are aligned by search-space-specific cell counting in `get_layer_metric_array_adv_feats`.
- Search orchestration (sampling + proxy ranking) is implemented in `main.py` + `sampling.py`.

## Comparison to Related Methods

- Compared with SynFlow/GradNorm (clean zero-shot proxies): CRoZe explicitly models robust alignment between clean and perturbed tasks.
- Compared with robust one-shot NAS (RobNet/AdvRush): CRoZe avoids adversarial supernet training and is much cheaper.
- Main advantage: Better robustness-cost tradeoff for architecture search.
- Main tradeoff: Proxy fidelity still depends on one-step approximation quality.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5, Table 6
- Key equation(s): Eq. (2) to Eq. (10)
- Key algorithm(s): Procedure described in Sec. 3 + search protocol in Sec. 4.3

## References

- arXiv: https://arxiv.org/abs/2306.05031
- HTML: https://arxiv.org/html/2306.05031
- Code: https://github.com/HyeonjeongHa/CRoZe
- Local implementation: D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations
