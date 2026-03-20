---
title: "ZiCo-BC"
type: method
source_paper: "ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks"
source_note: "[[ZiCo-BC]]"
authors: [Kartikeya Bhardwaj, Hsin-Pai Cheng, Sweta Priyadarshi, Zhuojin Li]
year: 2023
venue: ICCV Workshops
tags: [nas-method, nas, training-free, zero-cost-proxy, bias-correction]
created: 2026-03-20
updated: 2026-03-20
---

# ZiCo-BC

## One-line Summary
> ZiCo-BC corrects ZiCo's tendency to over-score deep, narrow repeated-block architectures by subtracting a structural penalty based on feature-map resolution and channel width.

## Source

- Paper: [ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks](https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html)
- PDF: https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf
- Code: Not publicly released during this run
- Paper note: [[ZiCo-BC]]

## Applicable Scenarios

- Problem type: Training-free ranking in micro-architecture NAS where candidates share a repeated-block family and differ mainly in width, repeats, kernel size, and conv type.
- Assumptions: Original ZiCo or a similar layer-summed gradient proxy exhibits a depth/width bias in the current search space.
- Data regime: Zero-shot proxy computation from task loss and a few forward/backward passes at initialization; no weight updates during scoring.
- Scale / constraints: Particularly useful when latency-aware evolutionary search must screen many candidates cheaply.
- Why it fits: The correction changes only the ranking score, so it can drop into an existing ZiCo-based search loop with almost no extra engineering.

## Not a Good Fit When

- Candidate architectures come from very different macro topologies, where a shared depth penalty may unfairly favor shallower families.
- Search spaces vary input resolution jointly with architecture size, since the current penalty assumes a fixed input size.
- You need a turnkey reproducible implementation right away; the paper does not release official ZiCo-BC code.

## Inputs, Outputs, and Objective

- Inputs: Candidate architecture `A`, task loss `L`, initialization-time gradient statistics from ZiCo, layer-wise feature-map sizes `(H_l, W_l, C_l)`, and penalty hyperparameter `\beta`.
- Outputs: Scalar corrected score `ZiCo-BC(A)` for ranking/search.
- Objective: Improve ranking quality and downstream latency/accuracy trade-offs by counteracting ZiCo's preference for thin, deep models.
- Core assumptions: In repeated-block spaces, the original ZiCo accumulation over layers systematically over-rewards depth relative to width.

## Method Breakdown

### Stage 1: Compute original ZiCo score
- Evaluate the base ZiCo proxy from gradient statistics at initialization, using multiple batches but no parameter updates.
- This reuses the original ZiCo computation unchanged.
- Source: Sec. 2, Eq. (1)

### Stage 2: Compute structural penalty
- For each layer, collect feature-map height `H_l`, width `W_l`, and channels `C_l`.
- Form the penalty term `\beta \sum_l \log(H_l W_l / \sqrt{C_l})`.
- Source: Sec. 3, Eq. (2)

### Stage 3: Rank architectures with corrected score
- Subtract the penalty from ZiCo to obtain `ZiCo-BC`.
- Use the corrected score inside the same search procedure used for the target task.
- Source: Sec. 3, Eq. (2); Sec. 4

### Stage 4: Search under task and hardware objectives
- For segmentation macro search and micro search, the paper uses NSGA-II evolutionary search with mobile latency in the loop.
- For classification/detection micro search, ZiCo-BC ranks candidates in EfficientNet/EfficientDet-style spaces before full training.
- Source: Sec. 2, Sec. 4, Table 1-4

## Pseudocode

```text
Algorithm: ZiCo-BC-guided micro-architecture search
Input: Candidate architecture A, task loss L, penalty coefficient beta, search loop S
Output: Ranked candidates or selected architecture A*

1. Initialize A without training updates and run the original ZiCo computation.
   Source: Sec. 2, Eq. (1)
2. For each layer l, read feature-map size (H_l, W_l, C_l).
   Source: Sec. 3, Eq. (2)
3. Compute penalty P(A) = beta * sum_l log(H_l W_l / sqrt(C_l)).
   Source: Sec. 3, Eq. (2)
4. Set ZiCo-BC(A) = ZiCo(A) - P(A).
   Source: Sec. 3, Eq. (2)
5. Use ZiCo-BC as the ranking signal inside the existing evolutionary or candidate-selection loop.
   Source: Sec. 2, Sec. 4; Inference from source
6. Fully train the selected architecture and evaluate task metrics/latency.
   Source: Sec. 4, Table 3-4; Inference from source
```

## Training Pipeline

1. Define the task-specific search space.
2. For each candidate, compute ZiCo gradient statistics with the task loss at initialization.
3. Apply the structural penalty to obtain ZiCo-BC.
4. Run the search loop and keep Pareto or top-ranked candidates.
5. Fully train selected architectures with the standard task recipe.

Sources:

- Sec. 2
- Sec. 3, Eq. (2)
- Sec. 4

## Inference Pipeline

1. Use ZiCo-BC only during the search stage; it is not a test-time model component.
2. After search, train the chosen architecture normally.
3. Deploy the trained architecture with ordinary forward inference.

Sources:

- Sec. 4
- Inference from source

## Complexity and Efficiency

- Time complexity: Same dominant order as ZiCo, since the new term only adds layer-wise shape bookkeeping and a log-sum penalty.
- Space complexity: Essentially unchanged from ZiCo.
- Runtime characteristics: The paper reports better searched models, but not a separate wall-clock overhead for the bias correction itself.
- Scaling notes: Increasing `\beta` pushes search away from maximal-depth solutions; the authors tune it by inspecting Pareto architectures.

## Implementation Notes

- Hyperparameter choice: `\beta = 1` for image classification and object detection; `\beta = 2` for semantic segmentation.
- Search heuristic: Inspect Pareto candidates; if many saturate at maximum depth with small width, increase `\beta`.
- Loss choice matters: the paper uses cross-entropy for classification, focal loss for object detection, and the FFNet training loss for segmentation search.
- Search spaces:
  - EfficientNet/EfficientDet: kernel size, channel size, repeats, regular vs group convolution.
  - FFNet-style segmentation: residual-block counts, stage widths, regular vs group convolution.
- Code status: No official ZiCo-BC repository was linked from the paper page during this run, so this note is paper-derived rather than code-verified.

## Comparison to Related Methods

- Compared with original ZiCo: keeps the same gradient proxy but explicitly penalizes architectures that are too deep and too narrow for the search space.
- Compared with manual scaling baselines: offers a search-based way to recover similar or better accuracy at lower latency.
- Main advantage: Very low-overhead correction with consistent improvements across benchmark correlation and three deployment-oriented vision tasks.
- Main tradeoff: It is a heuristic, search-space-specific correction rather than a new theoretically grounded universal proxy.

## Evidence and Traceability

- Key figure(s): Fig. 1
- Key table(s): Table 1, Table 2, Table 3, Table 4
- Key equation(s): Eq. (1), Eq. (2)
- Key algorithm(s): No separate algorithm block; search procedure described in Sec. 2 and Sec. 4

## References

- CVF HTML: https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html
- CVF PDF: https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf
- DOI: https://doi.org/10.1109/ICCVW60793.2023.00151
- Original ZiCo paper: https://openreview.net/forum?id=qGWsrQhL0S
- Original ZiCo code: https://github.com/SLDGroup/ZiCo
- Local implementation: Not archived
