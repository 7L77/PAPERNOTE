---
title: "ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks"
method_name: "ZiCo-BC"
authors: [Kartikeya Bhardwaj, Hsin-Pai Cheng, Sweta Priyadarshi, Zhuojin Li]
year: 2023
venue: ICCV Workshops
tags: [nas, training-free-nas, zero-cost-proxy, bias-correction, iccvw]
zotero_collection: ""
image_source: online
arxiv_html: https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html
local_pdf: D:/PRO/essays/papers/ZiCo-BC A Bias Corrected Zero-Shot NAS for Vision Tasks.pdf
created: 2026-03-20
---

# Paper Note: ZiCo-BC

## Meta
| Item | Content |
|---|---|
| Paper | ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks |
| CVF page | https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html |
| PDF | https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf |
| DOI | https://doi.org/10.1109/ICCVW60793.2023.00151 |
| Local PDF | `D:/PRO/essays/papers/ZiCo-BC A Bias Corrected Zero-Shot NAS for Vision Tasks.pdf` |
| Code | No official ZiCo-BC repository found during this run; note is paper-only |

## One-line Summary
> ZiCo-BC keeps ZiCo's gradient-statistics proxy but subtracts a depth/width/resolution penalty so zero-shot NAS stops over-favoring overly deep, narrow networks in repeated-block search spaces.

## Core Contributions
1. Validates that gradient-based [[Training-free NAS]] can perform direct macro-architecture search for semantic segmentation, not just image classification benchmarks (Sec. 2, Table 1).
2. Identifies a concrete [[Depth-Width Bias]] in ZiCo during repeated-block micro-architecture search: the score tends to prefer thinner and deeper models (Sec. 3, Fig. 1).
3. Proposes a simple corrected score `ZiCo-BC = ZiCo - \beta \sum_l \log(H_l W_l / \sqrt{C_l})`, adding a structural penalty based on feature-map size and channel width (Eq. 2).
4. Shows better ranking correlation on [[NATS-Bench-SSS]] and better latency/accuracy trade-offs on ImageNet, COCO detection, and Cityscapes segmentation (Table 2-4).

## Problem Context
### Target problem
- Search with [[Zero-Cost Proxy]] methods is fast, but rank quality can collapse when the proxy has structural bias.
- This paper studies the case where the original ZiCo metric rewards architectures that add depth faster than width in micro-architecture search spaces.

### Prior limitation
- Existing zero-shot NAS papers mostly evaluate on image classification or NAS benches instead of direct downstream search on detection/segmentation tasks.
- Even strong proxies can be biased toward particular architectural traits, which hurts the actual Pareto frontier found during search.

### Why ZiCo-BC
- The authors argue the original ZiCo score accumulates layer contributions in a way that scales favorably with depth.
- Adding a correction tied to `H_l`, `W_l`, and `C_l` discourages the "very deep and very thin" corner without changing the overall search framework.

## Method Details
### Original ZiCo view
ZiCo is the predecessor proxy from ICLR 2023. It uses gradient statistics at random initialization, aggregated across several batches, to estimate convergence/generalization quality without training updates.

- In this paper, the exact ZiCo equation is reused as the base proxy (Sec. 2, Eq. 1).
- Intuitively, it measures a layer-wise inverse coefficient-of-variation style gradient stability signal.

### Bias-corrected score
The core modification is Eq. (2):

$$
\mathrm{ZiCo\text{-}BC}
=
\mathrm{ZiCo}
- \beta \sum_{l=1}^{D} \log\left(\frac{H_l W_l}{\sqrt{C_l}}\right)
$$

- `H_l, W_l`: feature-map spatial resolution at layer `l`.
- `C_l`: channel width at layer `l`.
- `\beta`: penalty strength.

Interpretation:
- Deeper models accumulate more penalty terms.
- Narrower models have smaller `C_l`, increasing the penalty.
- Earlier high-resolution stages also contribute stronger penalty.

This is the mechanism the paper uses to counter ZiCo's preference for narrow/deep repeated-block architectures.

### Search settings
The paper studies two search regimes:
1. Macro-architecture search: heterogeneous backbone/head choices, exemplified by HRNet/FFNet segmentation search (Sec. 2).
2. Micro-architecture search: fixed family with repeated blocks, varying kernel size, width, repeats, and convolution type (Sec. 3-4).

The correction is meant for regime 2, not as a universal fix for regime 1.

## Key Experimental Evidence
### 1. Direct macro search on Cityscapes (Table 1)
- HRNet: `28.80 ms`, `77.0%` mIoU.
- Manual FFNet: `8.35 ms`, `79.7%` mIoU.
- ZiCo-searched model: `8.48 ms`, `80.7%` mIoU.

Takeaway:
- Even before introducing bias correction, ZiCo is already useful for direct downstream macro search on segmentation.

### 2. Ranking correlation on NATS-Bench-SSS (Table 2)
- CIFAR-10: Kendall `0.72 -> 0.78`, Spearman `0.91 -> 0.94`.
- CIFAR-100: Kendall `0.56 -> 0.60`, Spearman `0.76 -> 0.79`.
- ImageNet16-120: Kendall `0.73 -> 0.79`, Spearman `0.90 -> 0.94`.

Takeaway:
- The correction improves rank fidelity consistently in a size-search setting that matches the targeted micro-architecture regime.

### 3. EfficientNet-style ImageNet search (Table 3)
- Scaling baseline: `0.90 ms`, `77.7%`.
- ZiCo: `0.82 ms`, `76.8%`.
- ZiCo-BC: `0.80 ms`, `77.7%`.

Takeaway:
- ZiCo-BC keeps baseline accuracy while reducing latency by 11%, whereas original ZiCo loses about 0.9% accuracy.

### 4. EfficientDet-style COCO search (Table 3)
- Scaling baseline: `2.792 ms`, `33.6` mAP.
- ZiCo-BC: `1.974 ms`, `33.8` mAP.

Takeaway:
- The paper reports a 29% latency reduction while slightly improving detection accuracy.

### 5. FFNet-style Cityscapes micro search (Table 4)
- FFNet: `8.35 ms`, `79.70%`.
- ZiCo: `7.02 ms`, `78.62%`.
- ZiCo-BC: `7.44 ms`, `79.71%`.

Takeaway:
- ZiCo-BC finds a model with similar mIoU to FFNet but 11% lower latency, while plain ZiCo trades away too much accuracy.

## Practical Reading
### What is genuinely new here
- Not a brand-new zero-cost proxy family.
- The paper's contribution is a search-space-aware correction layer on top of an existing proxy.

### Why the idea works
- In repeated-block spaces, depth can be "counted" many times by a layer-summed proxy.
- A penalty based on spatial size and inverse width pulls the search back toward more balanced architectures.

### Why it matters
- This is a useful reminder that a high proxy correlation on standard NAS benches does not guarantee unbiased search behavior in a broader deployment-oriented search space.

## Limitations
1. The fix is explicitly targeted at micro-architecture search with repeated blocks; the paper does not claim it is universal for macro search (Sec. 5).
2. The correction assumes fixed input size, so it does not address depth/width/input-resolution co-scaling (Sec. 5).
3. `\beta` is chosen by inspecting Pareto candidates and tuning until intermediate-depth models appear, which is practical but heuristic (Sec. 5).
4. There is no public ZiCo-BC implementation linked from the paper page, so reproducibility still depends on rebuilding the search setup.

## Critical View
### Strengths
1. Very simple modification with clear intuition and almost no extra computational burden beyond ZiCo.
2. Evaluated on three real vision tasks instead of only benchmark tabular spaces.
3. Separates macro-search usefulness from micro-search bias, which is a helpful diagnostic framing.

### Weaknesses
1. The correction is hand-designed and only lightly justified theoretically.
2. The paper reports end results, but not a deeper ablation on why `H_l W_l / \sqrt{C_l}` is the right form versus other penalties.
3. Absence of released code makes the exact engineering recipe harder to verify.

## Related Concepts
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Coefficient of Variation]]
- [[Depth-Width Bias]]
- [[NATS-Bench-SSS]]
- [[NSGA-II]]
- [[Pareto Front]]
- [[Width-Depth Ratio]]

## References
- CVF HTML: https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html
- CVF PDF: https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf
- DOI: https://doi.org/10.1109/ICCVW60793.2023.00151
- Predecessor method: https://openreview.net/forum?id=qGWsrQhL0S
- Original ZiCo code (predecessor, not ZiCo-BC): https://github.com/SLDGroup/ZiCo
