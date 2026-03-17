---
title: "Padding-Robustness Interplay"
type: method
source_paper: "On the Interplay of Convolutional Padding and Adversarial Robustness"
source_note: "[[Padding-Robustness Interplay]]"
authors: [Paul Gavrikov, Janis Keuper]
year: 2023
venue: ICCV Workshop
tags: [nas-method, adversarial-robustness, cnn-padding]
created: 2026-03-17
updated: 2026-03-17
---

# Padding-Robustness Interplay

## One-line Summary
> This paper is an analysis protocol (not a new backbone) that isolates how convolution padding mode/size changes clean and adversarial robustness behavior under multiple attacks.

## Source
- Paper: [On the Interplay of Convolutional Padding and Adversarial Robustness](https://arxiv.org/abs/2308.06612)
- HTML: https://arxiv.org/html/2308.06612
- Code: Not reported in the paper as an official repository
- Paper note: [[Padding-Robustness Interplay]]

## Applicable Scenarios
- Problem type: Robustness-sensitive CNN design and ablation benchmarking.
- Assumptions: Same backbone/training pipeline can be reused while only padding variables change.
- Data regime: Supervised image classification (CIFAR-like).
- Scale / constraints: Moderate-scale experiments with repeated attack evaluations.
- Why it fits: It cleanly separates architectural boundary handling (padding) from attack/training effects.

## Not a Good Fit When
- You need a new state-of-the-art robust model architecture.
- You require direct transfer claims to transformers or detection/segmentation tasks.
- Your benchmark cannot afford multi-attack evaluation (APGD-CE + FAB + Square + AutoAttack).

## Inputs, Outputs, and Objective
- Inputs: Backbone (ResNet-20), padding mode, kernel size, training regime, attack suite.
- Outputs: Clean accuracy, per-attack robust accuracy, perturbation distributions, runtime overhead.
- Objective: Understand causal impact of padding choices on robustness and evaluation bias.
- Core assumptions: Boundary interaction between receptive fields and padded area influences attack behavior.

## Method Breakdown

### Stage 1: Controlled architecture/training grid
- Enumerate padding mode in {zeros, reflect, replicate, circular}.
- Enumerate kernel size in {3, 5, 7, 9} with same-padding size floor(k/2).
- Train both native and FGSM-based adversarially trained models.
- Source: Sec. 3, Training Details.

### Stage 2: Multi-attack robustness evaluation
- Evaluate APGD-CE, FAB, Square, and AutoAttack at low/high budgets.
- Compare both aggregate robustness and attack-specific rankings.
- Source: Sec. 3, Sec. 3.2, Table 2, Fig. 3.

### Stage 3: Mechanism and cost analysis
- Analyze perturbation boundary distributions (Fig. 4).
- Analyze explanation shifts with LayerCAM (Fig. 5).
- Benchmark padding/conv runtime overhead (Table 3).
- Test no-padding variants via upscaling/outpainting (Table 4).
- Source: Sec. 3.3, Sec. 3.4, Sec. 3.5, Sec. 3.6.

## Pseudocode

```text
Algorithm: Padding-Robustness Interplay Evaluation
Input: Dataset D, backbone B, padding modes M, kernel sizes K, attacks A, training regimes T
Output: Clean/robust metrics and mechanism diagnostics

1. For each t in T and each (m, k) in M x K, train model B_{t,m,k}.
   Source: Sec. 3, Training Details
2. For each trained model, evaluate clean accuracy and robustness under A.
   Source: Sec. 3.1, Sec. 3.2, Fig. 3, Table 2
3. For successful attacks, compute perturbation magnitude distributions along axes.
   Source: Sec. 3.3, Fig. 4
4. Compute LayerCAM shift maps between clean and adversarial samples.
   Source: Sec. 3.5, Fig. 5
5. Benchmark padding-only and padded-conv latency by mode.
   Source: Sec. 3.4, Table 3
6. Repeat with no-padding variants (None / None+Up / None+Out) and compare.
   Source: Sec. 3.6, Table 4
7. Report recommendations conditioned on training regime and attack protocol.
   Source: Sec. 4
```

## Training Pipeline
1. Preprocess CIFAR-10 with channel normalization and random horizontal flip.
2. Train ResNet-20 using SGD + Nesterov momentum for 75 epochs.
3. For adversarial training: use FGSM Linf 8/255 and early-stop by PGD robustness.
4. Keep 10-seed averages for core comparisons.

Sources:
- Sec. 3, Training Details

## Inference Pipeline
1. Generate attack samples under specified norm/budget.
2. Measure clean and robust accuracy per model configuration.
3. Aggregate over seeds and compare by padding mode/kernel.

Sources:
- Sec. 3.1, Sec. 3.2

## Complexity and Efficiency
- Time complexity: Not reported analytically.
- Space complexity: Not reported analytically.
- Runtime characteristics: Zero padding gives the fastest padded-conv runtime in their benchmark.
- Scaling notes: Increasing kernel size tends to improve robustness in their setup, but effect depends on training regime.

## Implementation Notes
- No official reference code was linked in the paper/arXiv page.
- Robustness conclusions depend strongly on attack protocol; AutoAttack alone can hide per-attack reversals.
- Circular padding is consistently poor under adversarial training in this study.
- No-padding alternatives reduce robustness despite attempts (upscale/outpaint) to recover resolution.

## Comparison to Related Methods
- Compared with [[Adversarial Training]]: This work studies architecture-level padding effects; it is not a replacement training algorithm.
- Compared with [[AutoAttack]] usage norms: It warns that aggregate benchmarks can bias ranking toward zero padding.
- Main advantage: Actionable architecture/testing guidance with concrete ablations.
- Main tradeoff: Evidence is limited to CIFAR-10 + ResNet-20.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 3, Fig. 4, Fig. 5, Fig. 6.
- Key table(s): Table 1, Table 2, Table 3, Table 4.
- Key equation(s): Eq. (1) adversarial objective.
- Key algorithm(s): No novel algorithm; protocol-driven empirical study.

## References
- arXiv: https://arxiv.org/abs/2308.06612
- HTML: https://arxiv.org/html/2308.06612
- Code: Not reported as official
- Local implementation: Not archived (no official paper code link found as of 2026-03-17)

