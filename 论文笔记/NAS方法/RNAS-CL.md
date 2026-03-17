---
title: "RNAS-CL"
type: method
source_paper: "Robust neural architecture search by cross-layer knowledge distillation"
source_note: "[[RNAS-CL]]"
authors: [Utkarsh Nath, Yancheng Wang, Yingzhen Yang]
year: 2023
venue: ICLR 2023 Workshop
tags: [nas-method, robustness, knowledge-distillation, differentiable-search]
created: 2026-03-17
updated: 2026-03-17
---

# RNAS-CL

## One-line Summary
> RNAS-CL searches robust compact architectures by jointly optimizing per-layer teacher assignment and per-block channel choices with differentiable Gumbel-Softmax under a latency-aware objective.

## Source
- Paper: [Robust neural architecture search by cross-layer knowledge distillation](https://openreview.net/forum?id=VQfWcqPjJP)
- PMLR: https://proceedings.mlr.press/v220/nath23a.html
- Code: https://github.com/Statistical-Deep-Learning/RNAS-CL
- Paper note: [[RNAS-CL]]
- Local code: `D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation`

## Applicable Scenarios
- Problem type: Robust image-classification NAS under model-size/MAC constraints.
- Assumptions: A robust teacher provides transferable intermediate cues for student robustness.
- Data regime: Supervised classification with adversarial evaluation; optional post-search adversarial training.
- Scale / constraints: FBNetV2-style supernet search where channel choices and teacher mappings are differentiable.
- Why it fits: It explicitly optimizes robustness and efficiency in one search procedure.

## Not a Good Fit When
- You need certified robustness guarantees.
- You do not have a robust teacher checkpoint.
- Your search space cannot be parameterized with differentiable architecture choices.

## Inputs, Outputs, and Objective
- Inputs: Dataset `D`, robust teacher `T`, supernet `S`, temperature schedule `tau`, loss weights (`gamma_s`, `gamma_t`), latency control term.
- Outputs: Final architecture and selected teacher mapping per student layer.
- Objective: Maximize clean/robust performance with low latency/compute.
- Core assumptions: Learned cross-layer tutor mapping improves student robustness.

## Method Breakdown

### Stage 1: Build teacher-student cross-layer search graph
- Define attention maps for intermediate activations and connect each student layer to all teacher layers with soft weights.
- Source: Sec. 3.1, Sec. 3.2, Fig. 2.

### Stage 2: Differentiable tutor search
- Parameterize tutor assignment by Gumbel-Softmax weights `g_ij`.
- Anneal temperature to move from soft mixing toward near one-hot tutor selection.
- Source: Sec. 3.2, Eq. (1) context.

### Stage 3: Differentiable channel/filter search
- Use Gumbel-style channel choices for each block (FBNetV2-inspired).
- Optimize architecture with latency/FLOPs proxy alongside prediction and distillation terms.
- Source: Sec. 3.3, Sec. 3.4.

### Stage 4: Finalize architecture and retrain
- Select top tutor per student layer (`argmax_j g_ij`) and final channel option per block.
- Retrain searched architecture with train-phase objective; optionally replace CE with TRADES objective.
- Source: Sec. 3.4, Sec. 4.1, Appendix A.3.

## Pseudocode
```text
Algorithm: RNAS-CL
Input: Robust teacher T, supernet S, dataset D, temperature schedule tau
Output: Searched robust architecture A and tutor mapping M

1. Initialize student supernet parameters and tutor-assignment logits.
   Source: Sec. 3.2, Fig. 2
2. For each search step:
   2.1 Compute student/teacher outputs and intermediate features.
       Source: Sec. 3.1, Sec. 3.4
   2.2 Build attention-alignment (or implementation-specific KD) term using Gumbel-soft tutor weights.
       Source: Sec. 3.2, Eq. (1); code: basic_blocks.py (kd_GS_thetas + gumbel_softmax)
   2.3 Update network and architecture parameters with latency-aware search loss.
       Source: Sec. 3.4 Eq. (2); code: search.py/search_loss
   2.4 Anneal temperature tau.
       Source: Appendix A.1; code: search.py (temperature *= exp(temp_factor))
3. Discretize tutor and channel selections via argmax.
   Source: Sec. 3.4 (after search); code: train.py/load_searched_model
4. Retrain final architecture with train loss (or TRADES variant).
   Source: Eq. (3), Sec. 4.1, Appendix A.3; code: train.py
```

## Training Pipeline
1. Search phase:
- Optimize model weights plus architecture/tutor Gumbel parameters.
- Use CE + KD-like term + latency term.
2. Discretization:
- Convert soft architecture choices to hard indices.
3. Train phase:
- Retrain searched model from scratch.
- Optionally use TRADES for stronger adversarial robustness.

Sources:
- Sec. 3.4, Sec. 4, Appendix A.1/A.3, code in `imageNetDA/search.py` and `imageNetDA/train.py`.

## Inference Pipeline
1. Use finalized discrete architecture only.
2. Standard forward prediction for clean samples.
3. Evaluate robustness via FGSM/PGD/MI-FGSM (paper protocol).

Sources:
- Sec. 4, Table 1, Appendix A.2.

## Complexity and Efficiency
- Tutor mapping search space is exponential (`n_t^{n_s}`), but relaxed optimization is differentiable with Gumbel-Softmax.
- Latency-aware term is optimized jointly in search objective.
- Reported models span very small to larger footprints (e.g., 0.11M to 11M params on CIFAR-10 variants).

## Implementation Notes
- Codebase has two-stage scripts:
- Search: `imageNetDA/search.py`
- Train: `imageNetDA/train.py`
- Temperature schedule in config: `base_temperature: 5.0`, `temp_factor: -0.045`.
- Practical caution: paper describes activation attention alignment, while code prominently computes KL terms over interpolated conv weights in core block implementation.

## Comparison to Related Methods
- Compared with [[DARTS]] / [[PC-DARTS]]:
- Adds explicit robustness-distillation and teacher-layer assignment search.
- Compared with robust pruning methods (Hydra/LWM):
- Better clean accuracy at similar or lower compute in reported ImageNet-100 settings.
- Main advantage:
- Robustness-efficiency tradeoff without requiring robust training during search.
- Main tradeoff:
- Depends on robust teacher and exact implementation details.

## Evidence and Traceability
- Key figure(s): Fig. 1-5.
- Key table(s): Table 1-4.
- Key equation(s): Eq. (1)-(3).
- Key algorithm(s): Differentiable tutor + channel search loop (Sec. 3.2-3.4).

## References
- OpenReview: https://openreview.net/forum?id=VQfWcqPjJP
- PMLR: https://proceedings.mlr.press/v220/nath23a.html
- Code: https://github.com/Statistical-Deep-Learning/RNAS-CL
- Local implementation: D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation
