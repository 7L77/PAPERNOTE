---
title: "Robust Principles"
type: method
source_paper: "Robust Principles: Architectural Design Principles for Adversarially Robust CNNs"
source_note: "[[Robust Principles]]"
authors: [ShengYun Peng, Weilin Xu, Cory Cornelius, Matthew Hull, Kevin Li, Rahul Duggal, Mansi Phute, Jason Martin, Duen Horng Chau]
year: 2023
venue: BMVC
tags: [nas-method, adversarial-robustness, cnn-architecture]
created: 2026-03-17
updated: 2026-03-17
---

# Robust Principles

## One-line Summary
> Robust Principles improves adversarial robustness of CNNs through three composable architectural rules: WD-ratio control, convolutional stem preference, and SE+non-parametric smooth activations.

## Source
- Paper: [Robust Principles: Architectural Design Principles for Adversarially Robust CNNs](https://arxiv.org/abs/2308.16258)
- HTML: https://arxiv.org/html/2308.16258
- Code: https://github.com/poloclub/robust-principles
- Paper note: [[Robust Principles]]

## Applicable Scenarios
- Problem type: Architecture-level robustness improvement for image classification CNNs under adversarial attacks.
- Assumptions: You can train/evaluate with adversarial objectives (Fast-AT/SAT/TRADES/MART, etc.).
- Data regime: Supervised image datasets, from CIFAR scale to ImageNet scale.
- Scale / constraints: Suitable when architecture redesign is possible and adversarial training cost is acceptable.
- Why it fits: It gives explicit architecture knobs and ranges, not just training-recipe changes.

## Not a Good Fit When
- You need certified robustness guarantees rather than empirical attack robustness.
- You cannot afford adversarial training/evaluation.
- Your model family is far from CNN-style staged backbones (e.g., pure token-only designs) without adaptation.

## Inputs, Outputs, and Objective
- Inputs: Baseline CNN architecture, attack budget `epsilon`, training recipe, and stage-wise width/depth candidates.
- Outputs: Robustified architecture variant (`Ra*`) with improved AA/PGD robustness.
- Objective: Improve adversarial accuracy while keeping clean accuracy and parameter budget competitive.
- Core assumptions: Robustness can be improved by rebalancing macro/micro architecture components.

## Method Breakdown

### Stage 1: Macro Rebalancing via WD Ratio
- Define width-depth ratio as average `W_i / D_i` over all body stages except the last.
- Search/reconfigure stage depths and widths so the model falls into the robust interval `[7.5, 13.5]`.
- Source: Sec. 4.1, Eq. (2), Fig. 2(a)

### Stage 2: Stem Redesign
- Replace patchify-style aggressive downsampling with convolutional stem + postponed downsampling.
- Increase stem output width (e.g., 64 -> 96) when budget allows.
- Source: Sec. 4.2, Fig. 2(b)

### Stage 3: Residual Block Robustification
- Insert SE block after `3x3` conv and use low reduction ratio (`r=4` recommended).
- Replace ReLU with non-parametric smooth activations (SiLU preferred, GELU also strong).
- Source: Sec. 4.3.1, Sec. 4.3.2, Table 1

### Stage 4: End-to-End Validation Across Recipes/Scales
- Train robustified models with multiple AT methods and evaluate by PGD + AutoAttack.
- Verify gains on CIFAR-10/100 and ImageNet, across ResNet/WRN and parameter scales.
- Source: Sec. 5, Table 2, Table 3

## Pseudocode
```text
Algorithm: Robust Principles Architecture Robustification
Input: Baseline CNN A, dataset D, attack setup B, training recipe T
Output: Robustified CNN A_ra

1. Compute stage-wise WD ratio of A:
   WD = (1/(n-1)) * sum_{i=1}^{n-1} (W_i / D_i).
   Source: Eq. (2)
2. Adjust stage depths/widths to place WD in [7.5, 13.5].
   Source: Sec. 4.1, Fig. 2(a)
3. Replace stem with convolutional stem and postponed downsampling;
   optionally widen stem channels.
   Source: Sec. 4.2, Fig. 2(b)
4. Add SE block after 3x3 conv with low reduction ratio (r=4),
   and replace ReLU with SiLU (or GELU).
   Source: Sec. 4.3.1, Sec. 4.3.2
5. Train A_ra with adversarial training recipe T (Fast-AT/SAT/TRADES/MART).
   Source: Sec. 3 (training setup), Sec. 5
6. Evaluate with PGD and AutoAttack; compare against baseline A.
   Source: Sec. 3 (attacks), Table 1/2/3
7. If gains hold, keep architecture; otherwise re-tune WD/stem/SE/activation.
   Source: Inference from source (engineering loop)
```

## Training Pipeline
1. Build model via Hydra config (`model=model` plus overrides in `MODEL.mk`).
2. Create adversary (`LinfPGDAttack`) for inner maximization during training.
3. Run FAT or SAT loops in `robustarch/adv_train.py`.
4. Evaluate natural, PGD, and AutoAttack metrics.

Sources:
- Paper: Sec. 3, Sec. 5
- Code: `robustarch/main.py`, `robustarch/adv_train.py`, `MODEL.mk`

## Inference Pipeline
1. Load trained checkpoint.
2. Run clean validation and adversarial validation (PGD/AA).
3. Report clean, AA, PGD-k-e metrics at configured `epsilon`.

Sources:
- Paper: Sec. 3 (attack definitions), Sec. 5
- Code: `test_natural`, `test_pgd` in `robustarch/adv_train.py`; AA branch in `robustarch/main.py`

## Complexity and Efficiency
- Time complexity: Dominated by adversarial training and attack evaluation; architecture changes themselves are cheap.
- Space complexity: Similar to baseline plus modest overhead from SE and widened stem.
- Runtime characteristics: Fast-AT is used in paper for scalable ImageNet exploration.
- Scaling notes: Gains persist across 26M to 267M (paper tables), including cases with fewer parameters but better robustness.

## Implementation Notes
- Local code path: `D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs`.
- `MODEL.mk` explicitly encodes robustified variants:
  - `RaResNet50`, `RaResNet101`, `RaWRN101_2`.
  - Key overrides: `depths`, `group_widths`, `stem_width=96`, postponed downsampling, `se_ratio=0.25`, activation to `torch.nn.SiLU`.
- `robustarch/models/model.py` implements configurable stages, SE insertion, and activation layers.
- `robustarch/adv_train.py` applies PGD inner maximization during training and PGD/AA evaluation at test time.
- Paper-code alignment: The architectural principles map directly to config overrides; no major conceptual mismatch observed.

## Comparison to Related Methods
- Compared with [[RobNet]]: Robust Principles gives hand-designed transferable rules; RobNet searches robust structures via NAS.
- Compared with pure training-recipe improvements: This method changes architecture itself and composes with those recipes.
- Main advantage: Simple and reproducible architecture knobs with consistent gains.
- Main tradeoff: Still empirical robustness, with significant adversarial training cost.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2
- Key table(s): Table 1, Table 2, Table 3
- Key equation(s): Eq. (1), Eq. (2)
- Key algorithm(s): No standalone algorithm block in paper; procedure synthesized from Sec. 4-5.

## References
- arXiv: https://arxiv.org/abs/2308.16258
- HTML: https://arxiv.org/html/2308.16258
- Code: https://github.com/poloclub/robust-principles
- Local implementation: D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs

