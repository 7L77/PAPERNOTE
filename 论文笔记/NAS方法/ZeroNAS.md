---
title: "ZeroNAS"
type: method
source_paper: "ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning"
source_note: "[[ZeroNAS]]"
authors: [Caixia Yan, Xiaojun Chang, Zhihui Li, Weili Guan, Zongyuan Ge, Lei Zhu, Qinghua Zheng]
year: 2022
venue: TPAMI
tags: [nas-method, zero-shot-learning, gan, differentiable-nas]
created: 2026-03-17
updated: 2026-03-17
---

# ZeroNAS

## One-line Summary

> ZeroNAS jointly searches generator and discriminator architectures for ZSL feature generation via differentiable adversarial bi-level optimization, then prunes the supernet into compact dataset-specific GANs.

## Source

- Paper: [ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning](https://doi.org/10.1109/TPAMI.2021.3127346)
- HTML: Not provided by the paper (IEEE article page)
- Code: https://github.com/caixiay/ZeroNAS
- Paper note: [[ZeroNAS]]

## Applicable Scenarios

- Problem type: Search GAN architectures for feature-generation-based [[Zero-Shot Learning]] / [[Generalized Zero-Shot Learning]].
- Assumptions: Semantic class embeddings are available and GAN-generated CNN features can support downstream softmax classification.
- Data regime: Supervised seen classes, unseen classes only at test time.
- Scale / constraints: Works when full RL-style GAN NAS is too expensive and a differentiable search surrogate is preferred.
- Why it fits: It models G/D coupling directly during search instead of searching only one side.

## Not a Good Fit When

- You need strong cross-dataset architecture transfer without re-search.
- Your pipeline is pixel-level generation rather than feature-level synthesis.
- You cannot run adversarial search loops with alternating updates and gradient penalty.

## Inputs, Outputs, and Objective

- Inputs: Seen-class visual features `x`, class semantics `c_y`, Gaussian noise `z`, search-space DAG, candidate FC operations.
- Outputs: Discrete `genotype_G` and `genotype_D`, trained GAN models, synthesized unseen features, ZSL/GZSL classifier accuracy.
- Objective: Maximize ZSL/GZSL performance by jointly optimizing architecture and network parameters of G/D.
- Core assumptions: Better G/D architectural compatibility yields better unseen-feature distribution matching.

## Method Breakdown

### Stage 1: Build differentiable MLP supernet for G/D

- Use DAG nodes with mixed operations on each edge.
- Edge importance and operation importance are both softmax-weighted.
- Source: Sec. 3.2, Eq. (2), Eq. (3), Fig. 2.

### Stage 2: Adversarial bi-level architecture search

- Lower-level: optimize network parameters `u_g/u_d` using train split.
- Upper-level: optimize architecture weights `v_g/v_d` using validation split.
- Source: Sec. 3.3, Eq. (5), Algorithm 1.

### Stage 3: Four-step alternating optimization per loop

- Update order: `v_d` on validation -> `u_d` on training -> `v_g` on validation -> `u_g` on training.
- Source: Algorithm 1, Eq. (6)-(9), code `clswgan.py`.

### Stage 4: Prune supernet to discrete architecture

- Keep top-2 incoming edges per intermediate node.
- Keep top-1 operation on each retained edge.
- Source: Sec. 3.4; code evidence in `model.py:get_cur_genotype()`.

### Stage 5: Retrain and evaluate

- Retrain searched architecture from scratch on full train set.
- Generate unseen-class features and train a softmax classifier for ZSL/GZSL.
- Source: Sec. 3.4, Eq. (10)-(11), Table 1-2; code `clswgan_retrain.py` + `generate_feature.py`.

## Pseudocode

```text
Algorithm: ZeroNAS
Input: Seen data D_tr, semantic embeddings C, noise prior p(z)
Output: Searched genotype_G, genotype_D and final ZSL/GZSL predictor

1. Construct MLP DAG supernets for G and D with mixed FC operations.
   Source: Sec. 3.2, Fig. 2
2. Initialize network params (u_g, u_d) and architecture params (v_g, v_d).
   Source: Algorithm 1
3. Repeat until convergence:
   3.1 Update v_d using validation WGAN-GP objective.
       Source: Eq. (6), Algorithm 1
   3.2 Update u_d using training WGAN-GP objective.
       Source: Eq. (7), Algorithm 1
   3.3 Update v_g using validation generator+classification objective.
       Source: Eq. (8), Algorithm 1
   3.4 Update u_g using training generator+classification objective.
       Source: Eq. (9), Algorithm 1
4. Derive discrete architectures by top-2 edge pruning + top-1 op pruning.
   Source: Sec. 3.4
5. Retrain derived G/D from scratch, synthesize unseen features, train softmax classifier.
   Source: Sec. 3.4, Eq. (10)-(11)
```

## Training Pipeline

1. Pretrain seen-class classifier `C` for classification-guided GAN loss.
2. Split seen data into train/valid for architecture search.
3. Run alternating G/D architecture+weight optimization with WGAN-GP and cls loss.
4. Export best genotype pair and retrain with full train split.
5. Generate unseen features and train/evaluate ZSL or GZSL classifier.

Sources:

- Sec. 3.1-3.4, Algorithm 1.
- Code: `clswgan.py`, `clswgan_retrain.py`, `classifier.py`, `classifier2.py`.

## Inference Pipeline

1. For unseen class embedding `c_y`, sample `z ~ N(0,1)` and synthesize `x~ = G(z, c_y)`.
2. Build synthetic unseen set (or seen+unseen for GZSL).
3. Run trained softmax classifier to predict labels for query features.

Sources:

- Sec. 3.4, Eq. (10), Eq. (11).
- Inference from source (serving API is not separately formalized in paper).

## Complexity and Efficiency

- Time complexity: Not reported as closed-form.
- Space complexity: Not reported as closed-form.
- Runtime characteristics: Search is much cheaper than RL-style GAN NAS; paper reports about 1.5 GPU hours (FLO) and 2 GPU hours (CUB).
- Scaling notes: Architecture quality is dataset-dependent; transfer to other datasets degrades notably.

## Implementation Notes

- Search-space hidden dims in code:
  - Generator: `[128, 256, 512, 1024, 2048]`.
  - Discriminator: `[1024, 512, 256, 128, 1]`.
- Candidate ops in code match paper family: FC + (ReLU/LeakyReLU/BN/Dropout) combinations.
- Code uses separate optimizers for architecture weights (`alpha_optimizer_*`) and model weights (`weight_optimizer_*`) for both G and D.
- Validation split is constructed by random 50/50 split from seen training set in `clswgan.py`.
- Retrain stage requires manually setting `genotype_G`/`genotype_D` in `clswgan_retrain.py`.
- Environment note: official repo targets Python 3.6 and PyTorch 0.3.1.

## Comparison to Related Methods

- Compared with [[AutoGAN]] / AGAN: avoids RL controller and expensive candidate evaluation loops.
- Compared with DEGAS: searches both generator and discriminator, not generator only.
- Compared with [[f-CLSWGAN]]: architecture is searched instead of hand-crafted while preserving feature-generation paradigm.
- Main advantage: consistent ZSL/GZSL gains across multiple GAN baselines.
- Main tradeoff: searched architectures are less transferable across datasets.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6.
- Key table(s): Table 1, Table 2, Table 3.
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (5), Eq. (6)-(11).
- Key algorithm(s): Algorithm 1.

## References

- DOI: https://doi.org/10.1109/TPAMI.2021.3127346
- Code: https://github.com/caixiay/ZeroNAS
- Local implementation: D:/PRO/essays/code_depots/ZeroNAS Differentiable Generative Adversarial Networks Search for Zero-Shot Learning

