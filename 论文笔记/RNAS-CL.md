---
title: "Robust neural architecture search by cross-layer knowledge distillation"
method_name: "RNAS-CL"
authors: [Utkarsh Nath, Yancheng Wang, Yingzhen Yang]
year: 2023
venue: ICLR 2023 Workshop
tags: [nas, adversarial-robustness, knowledge-distillation, gumbel-softmax, latency-aware-search]
zotero_collection: ""
image_source: local-pdf
arxiv_html: https://openreview.net/forum?id=VQfWcqPjJP
local_pdf: D:/PRO/essays/papers/Robust neural architecture search by cross-layer knowledge distillation.pdf
local_code: D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation
created: 2026-03-17
---

# Paper Note: RNAS-CL

## Metadata
| Item | Value |
|---|---|
| Paper | Robust neural architecture search by cross-layer knowledge distillation |
| Venue | ICLR 2023 Workshop on Pitfalls of Limited Data and Computation for Trustworthy ML |
| OpenReview | https://openreview.net/forum?id=VQfWcqPjJP |
| PMLR Page | https://proceedings.mlr.press/v220/nath23a.html |
| Code | https://github.com/Statistical-Deep-Learning/RNAS-CL |
| Local PDF | `D:/PRO/essays/papers/Robust neural architecture search by cross-layer knowledge distillation.pdf` |
| Local Code | `D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation` |

## One-Line Summary
> RNAS-CL jointly searches channel configuration and teacher-student layer alignment so a compact student can inherit robustness signals from a robust teacher during NAS.

## Core Contributions
1. Proposes [[Cross-Layer Knowledge Distillation]] inside NAS: each student layer learns from a searched tutor layer rather than a fixed last-layer teacher signal (Sec. 3.2, Fig. 2).
2. Uses differentiable [[Gumbel-Softmax]] for two coupled searches: tutor mapping and channel/filter choices (Sec. 3.2-3.3).
3. Shows strong robustness-size tradeoff on CIFAR-10 and ImageNet-100, especially against FGSM/PGD/MI-FGSM attacks (Sec. 4, Table 1/2, Fig. 3/4).

## Problem Setting
### Target problem
- Search an architecture that is both efficient and robust under adversarial attacks.

### Why prior work is insufficient
- Standard NAS often optimizes clean accuracy but not robustness.
- Standard KD usually distills final outputs only; it does not search fine-grained layer-level teaching assignments.
- Robust models can be large and expensive.

### Key intuition
- A robust teacher contains useful intermediate spatial cues.
- If student layers can automatically choose the best teacher layer, the searched architecture can become robust without requiring robust training in the search phase.

## Method Details
### Attention map definition (Sec. 3.1)
- For activation tensor `A in R^{C x H x W}`, attention map is:

$$
[F(A)]_{h,w} = \sum_{c=1}^{C} A_{c,h,w}^2
$$

- This is the same family of activation-based attention transfer as in AT.

### Tutor search with Gumbel-Softmax (Sec. 3.2)
- Each student layer `i` has a distribution `g_ij` over all teacher layers `j`.
- Soft selections are optimized during search; near one-hot mappings are obtained as temperature decays.
- Search space size is exponential (`n_t^{n_s}`), so differentiable relaxation is essential.

### Architecture search for efficiency (Sec. 3.3)
- Channel/filter options per block are also selected via Gumbel weights.
- FLOPs/latency proxy is incorporated so optimization remains hardware-aware.
- Design follows [[FBNetV2]]-style supernet search.

### Losses (Sec. 3.4)
1. Attention alignment:

$$
L_{Attn}(A_t,A_s) = \frac{1}{n_s n_t}\sum_{i=1}^{n_s}\sum_{j=1}^{n_t}
g_{ij}\left\|
\frac{F(A^i_s)}{\|F(A^i_s)\|_2}-
\frac{F(A^j_t)}{\|F(A^j_t)\|_2}
\right\|_2^2
$$

2. Search loss (paper):

$$
L_{search} = \big(-y\log p + KL(p,q) + \gamma_s L_{Attn}\big)n_f
$$

3. Train loss (paper):

$$
L_{train} = -y\log p + KL(p,q) + \gamma_t L_{Attn}
$$

Where `p/q` are student/teacher output distributions, and `n_f` is the latency-related term.

## Main Evidence
### Figures
- Figure 1: Clean-vs-robustness frontier on CIFAR-10.
- Figure 2: Full training/search paradigm and cross-layer mapping illustration.
- Figure 3/4: Robustness curves across perturbation budgets on CIFAR-10 and ImageNet-100.
- Figure 5 (appendix): FBNetV2-like per-layer architecture search mechanism.

### Tables and key numbers
- Table 1 (CIFAR-10):
- `RNAS-CL-S7-WRT-34`: Clean 90.62, FGSM 48.93, PGD20 37.24, MI-FGSM 42.27, Params 0.32M.
- `RNAS-CL-M-WRT-34`: Clean 92.46, FGSM 50.51, PGD20 39.84, MI-FGSM 44.54, Params 3M.
- `RNAS-CL-L-WRT-34`: Clean 92.6, FGSM 52.37, PGD20 41.9, MI-FGSM 46.66, Params 11M.

- Table 2 (ImageNet-100, appendix):
- Without TRADES retraining, clean accuracy is high but PGD20 is weak.
- With [[TRADES]] retraining, adversarial accuracy improves a lot while keeping strong clean accuracy and lower MACs than pruning baselines.

## Code Cross-Check (Archived Repo)
Local repo: `D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation`

1. Search entrypoint:
- `imageNetDA/search.py` runs teacher loading, supernet search, Gumbel temperature annealing, and latency-aware objective.

2. Training entrypoint:
- `imageNetDA/train.py` loads searched model and supports CE/TRADES/multi-adv training variants.

3. Cross-layer matching signal in code:
- `mobile_cv/arch/fbnet_v2/basic_blocks.py` defines `kd_GS_thetas`, applies `gumbel_softmax`, and computes weighted KL terms against teacher weights.

4. Note on paper-code gap:
- Paper Sec. 3 emphasizes activation attention maps.
- The public code path prominently uses weight-level KL alignment with teacher conv weights in core blocks.
- This likely reflects an implementation simplification/variant; reproducibility notes should treat this as a potential mismatch to verify experimentally.

## Strengths, Limits, and Practical Notes
### Strengths
1. Clear robustness-efficiency objective in one search loop.
2. Layer-wise tutor assignment is more expressive than fixed-layer KD.
3. Solid empirical profile across CIFAR-10 and ImageNet-100.

### Limits
1. Robustness gains depend heavily on teacher quality and search-space design.
2. Reported implementation is tightly coupled to FBNet-style pipeline.
3. Paper-code mismatch (attention-map vs weight-KL emphasis) can affect faithful reproduction.

### Practical takeaways
1. If you want compact robust models, RNAS-CL is a useful baseline before full robust retraining.
2. For best robustness, run post-search adversarial training (e.g., TRADES), as paper appendix indicates.
3. When reproducing, pin exact loss definitions from code, not only paper equations.

## Related Concepts
- [[Robust Neural Architecture Search]]
- [[Knowledge Distillation]]
- [[Cross-Layer Knowledge Distillation]]
- [[Attention Map]]
- [[Gumbel-Softmax]]
- [[KL Divergence]]
- [[TRADES]]
- [[FGSM]]
- [[PGD Attack]]
- [[MI-FGSM]]
- [[FBNetV2]]
