---
title: "AdvRush: Searching for Adversarially Robust Neural Architectures"
method_name: "AdvRush"
authors: [Jisoo Mok, ByungMin Kim, Jihoon Park, Sungroh Yoon]
year: 2021
venue: ICCV
tags: [nas, robust-nas, adversarial-robustness, differentiable-nas]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2108.01289
local_pdf: D:/PRO/essays/papers/AdvRush Searching for Adversarially Robust Neural Architectures Supplemental.pdf
created: 2026-03-15
---

# 论文笔记：AdvRush

## 元信息
| Item | Value |
|---|---|
| Paper | AdvRush: Searching for Adversarially Robust Neural Architectures |
| arXiv | https://arxiv.org/abs/2108.01289 |
| ICCV page | https://openaccess.thecvf.com/content/ICCV2021/html/Mok_AdvRush_Searching_for_Adversarially_Robust_Neural_Architectures_ICCV_2021_paper.html |
| Main PDF | Not archived locally in this run |
| Supplement PDF (local) | `D:/PRO/essays/papers/AdvRush Searching for Adversarially Robust Neural Architectures Supplemental.pdf` |
| Original source PDF | `D:/PRO/essays/papers/Mok_AdvRush_Searching_for_ICCV_2021_supplemental.pdf` |
| Official code | Not found in CVF/arXiv/supplement links during this run |

## 一句话总结
> AdvRush keeps DARTS-style bilevel NAS, but adds an input-loss-landscape smoothness term (largest Hessian eigenvalue) into architecture optimization after warm-up, yielding architectures with stronger adversarial robustness.

## 核心贡献
1. Introduces a smoothness-oriented architecture regularizer based on the largest Hessian eigenvalue of input loss landscape.  
Source: Sec. 3.2, Eq. (9)-(10) in main paper.
2. Uses a two-phase search schedule: warm-up with vanilla DARTS objective, then architecture update with `L_val + gamma * L_lambda`.  
Source: Algorithm 1 in supplement (App. A1).
3. Shows consistent robustness gains over PDARTS and additional DARTS variants under adversarial training/evaluation.  
Source: Main paper Table 2/3; supplement Table A2/A3/A5.

## 问题背景
- Robust NAS methods often rely on expensive adversarial search or direct adversarial optimization of both weights and architecture, which increases cost.  
Source: Sec. 1-2 in main paper.
- The paper asks whether smoother input loss landscapes at search time can bias architecture toward robustness with lower additional cost.  
Source: Sec. 3.1-3.2 in main paper.

## 方法拆解

### 1) Input loss landscape smoothness regularization
- Compute Hessian of loss w.r.t. input:
  - `H = ∇_x^2 l(f_A(x), y)`  
  Source: Eq. (9), Sec. 3.2.
- Define smoothness regularizer via expected largest eigenvalue:
  - `L_lambda = E_(x,y)[lambda_max(H)]`  
  Source: Eq. (10), Sec. 3.2.
- Intuition: lower curvature around inputs means flatter loss landscape and better resistance to small perturbations.  
  Source: Sec. 3.1-3.2, Fig. 2 in main paper.

### 2) Search objective and schedule
- Before warm-up ends: same as DARTS updates for weights and architecture.
- After warm-up: architecture step uses validation loss plus smoothness term:
  - update `alpha` with gradient of `[L_val + gamma * L_lambda]`.
- Final architecture is discretized by the DARTS rule.  
Source: Algorithm 1, App. A1 (supplement).

### 3) Search space and model construction
- Search operators follow DARTS: zero, skip-connect, avg/max pool, sep conv (3x3/5x5), dilated conv (3x3/5x5).
- Final network stacks 18 normal cells + 2 reduction cells, with reductions at 1/3 and 2/3 depth.  
Source: App. A1 and Fig. A2/A3 (supplement).

## 关键公式（含解释）

### Eq. (9): Input-Hessian
`H = ∇_x^2 l(f_A(x), y)`

- `x`: input image
- `y`: label
- `f_A`: network defined by architecture `A`
- `l`: training loss
- `H`: local curvature of loss around input
Source: Sec. 3.2, Eq. (9).

### Eq. (10): Smoothness regularizer
`L_lambda = E_(x,y)[lambda_max(H)]`

- `lambda_max(H)` is the largest Hessian eigenvalue.
- Smaller `L_lambda` means smoother local landscape.  
Source: Sec. 3.2, Eq. (10).

### Architecture optimization term in search
`J(alpha) = L_val + gamma * L_lambda` (after warm-up)

- `gamma` controls robustness-vs-accuracy trade-off.
- Introduced after warm-up to avoid early instability.  
Source: Algorithm 1 (supplement) + Sec. 3.2 text.

## 关键图表与结果

### Main paper highlights
- Compared with robust NAS baselines, AdvRush reports improved robust accuracy under PGD/C&W/AutoAttack while keeping strong clean accuracy.  
Source: Table 2/3 in main paper.

### Supplement highlights
- Fig. A1: once `L_lambda` is activated, AdvRush drops `L_lambda` faster than DARTS, supporting smoothness effect.
- Table A2/A5: gamma ablation shows trade-off; default `gamma=0.01` keeps best clean/robust balance overall.
- Table A3: additional DARTS variants (`PGD Search`, longer-epoch DARTS) still underperform AdvRush in robust metrics.
- Fig. A2/A3: searched cells under adversarial training tend to include more skip/pooling/dilated patterns than PDARTS examples.
- Fig. A6: robustness trends across CIFAR-100/SVHN/Tiny-ImageNet under varying PGD iteration counts.

## 实验与实现细节
- Adversarial training optimizer: SGD, momentum 0.9, weight decay `1e-4`.
- Epochs: 200 for CIFAR/SVHN, 90 for Tiny-ImageNet.
- LR schedule:
  - CIFAR: 0.1 with decay at (100, 150)
  - SVHN: 0.01 with decay at (100, 150)
  - Tiny-ImageNet: 0.1 with decay at (30, 60)
- Datasets in supplement summary:
  - CIFAR-10/100: 50k train, 10k test, 32x32
  - SVHN: 73,257 train, 26,032 test, 32x32
  - Tiny-ImageNet: 100k train, 5k val, 5k test, 64x64  
Source: Table A1/A6.

## 批判性思考
### 优点
1. Minimal change to DARTS pipeline but measurable robustness gain.
2. Explicit smoothness signal (`lambda_max`-based) is conceptually interpretable.
3. Supplement includes practical ablations for `gamma` and alternative baselines.

### 局限
1. Official code repository is not clearly linked in CVF/arXiv/supp PDF metadata.
2. Hessian-eigenvalue-related computation may still add cost and approximation noise.
3. This run only had local supplemental PDF; main-PDF local archival is still missing.

### 可复现性
- [ ] Official code repo linked and archived
- [x] Search algorithm pseudocode available
- [x] Hyperparameters and datasets listed in supplement
- [ ] End-to-end local reproduction script verified

## 关联概念
- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Adversarial Robustness]]
- [[Input Loss Landscape]]
- [[PGD Attack]]
- [[FGSM]]
- [[Harmonic Robustness Score]]
