---
title: "On the Interplay of Convolutional Padding and Adversarial Robustness"
method_name: "Padding-Robustness Interplay"
authors: [Paul Gavrikov, Janis Keuper]
year: 2023
venue: ICCV Workshop
tags: [adversarial-robustness, cnn, padding, cifar-10]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2308.06612
local_pdf: D:/PRO/essays/papers/On the Interplay of Convolutional Padding and Adversarial Robustness.pdf
created: 2026-03-17
---

# Paper Note: Padding-Robustness Interplay

## Metadata
| Item | Value |
|---|---|
| Paper | On the Interplay of Convolutional Padding and Adversarial Robustness |
| Authors | Paul Gavrikov, Janis Keuper |
| Venue | ICCV Workshop, 2023 |
| arXiv | https://arxiv.org/abs/2308.06612 |
| HTML | https://arxiv.org/html/2308.06612 |
| Local PDF | `D:/PRO/essays/papers/On the Interplay of Convolutional Padding and Adversarial Robustness.pdf` |
| Code | Not found as an official paper repository (checked paper text + arXiv + CatalyzeX on 2026-03-17) |

## One-sentence Summary
> The paper shows that [[Convolutional Padding]] choices strongly change measured [[Adversarial Robustness]], and that default zero padding is often favored by [[AutoAttack]] ranking but is not uniformly best once attacks are separated.

## Core Contributions
1. First focused study of padding mode/size vs robustness in CNNs (Sec. 1, Sec. 3).
2. Demonstrates attack perturbation anomalies near image boundaries and links them to padding behavior (Fig. 1, Fig. 4, Sec. 3.3).
3. Evaluates padding-free alternatives (upscaling/outpainting) and shows they usually hurt robustness (Sec. 3.6, Table 4).

## Problem Setup
### Target Question
How do padding mode (`zeros`, `reflect`, `replicate`, `circular`) and kernel size affect clean accuracy and robustness under different attacks/training regimes?

### Experimental Design
- Backbone: ResNet-20 on CIFAR-10 (Sec. 3).
- Padding modes: `zeros`, `reflect`, `replicate`, `circular`.
- Kernel sizes: k in {3, 5, 7, 9}, with same padding size floor(k/2).
- Attacks: APGD-CE, FAB, Square, and AutoAttack aggregation.
- Two regimes:
  - Native training (no adversarial defense).
  - [[Adversarial Training]] with FGSM Linf 8/255 (early-stop by PGD robustness).

## Key Formula
### Adversarial Objective (Eq. 1)
The attack solves:

`max_{x' in B_epsilon(x)} L(F(x', theta), y)`

where `B_epsilon(x)` is the norm-bounded ball around input `x`.

Meaning:
- The attacker searches for a small perturbation that maximizes loss.
- Robustness is measured by whether prediction stays correct under this worst-case perturbation.

## Key Results (with numbers)
### 1) Clean Accuracy (Table 1)
- Without adversarial training:
  - Zero padding is best across k=3/5/7/9 (e.g., 90.26 at k=3 vs 90.10/90.13/90.15).
- With adversarial training:
  - Non-zero padding can be better at common small kernels.
  - At k=3: `reflect` 73.11 > `zeros` 71.84 (+1.27).

### 2) AutoAttack Robust Accuracy (Table 2)
- Without adversarial training:
  - Zero padding wins at all tested k (e.g., k=9: 39.18 vs 30.52/36.39/34.81).
- With adversarial training:
  - Zero remains slightly highest in AutoAttack aggregate (k=3: 36.88 vs 32.09/35.91/36.82),
  - but per-attack analysis (Sec. 3.2, Fig. 3) shows `reflect`/`replicate` can match or beat zero depending on attack and kernel.

### 3) Attack-wise Behavior (Fig. 3, Sec. 3.2)
- Native models:
  - Zero often dominates under low budgets.
  - Larger kernels improve robustness strongly in this setup.
- Adversarially trained models:
  - Ranking becomes attack-dependent.
  - `circular` is consistently the worst option.
  - Zero is never best on average over all attacks, but often best on APGD-CE.

### 4) Perturbation Distribution (Fig. 4, Sec. 3.3)
- Successful attacks show boundary anomalies, especially for Linf attacks.
- Under adversarial training, these anomalies weaken but do not disappear.
- Padding mode changes perturbation area-under-curve and boundary intensity.

### 5) Runtime Cost (Table 3, Sec. 3.4)
- Only padding op time (us): zeros 21.87, reflect 12.55, replicate 10.10, circular 56.96.
- Full padded conv time (us): zeros 55.65 (fastest), reflect 76.86, replicate 74.04, circular 132.60.
- Practical take: reflect/replicate may improve some metrics but add inference/training overhead.

### 6) No-padding Variants (Table 4, Sec. 3.6)
- Removing padding degrades both clean and robust metrics overall.
- Upscaling/outpainting recover some clean accuracy but robustness drops sharply.
- Conclusion: do not remove padding as a default robustness strategy.

## Critical Reading
### Strengths
1. Careful factorial design (padding x kernel x training x attack).
2. Reports both aggregate and per-attack behavior, exposing metric bias.
3. Connects performance with perturbation distribution and explanation shifts ([[LayerCAM]]).

### Limitations
1. Dataset scope is only CIFAR-10 (paper states this explicitly in Limitations).
2. Architecture scope is only ResNet-20.
3. No official code link in the paper, making exact replication harder.

### Practical Takeaways
1. If you benchmark only with [[AutoAttack]], you may over-prefer zero padding because APGD-CE ordering matters.
2. For adversarial training scenarios, test `reflect`/`replicate` explicitly instead of defaulting to zero.
3. Keep padding; avoid padding-free shortcuts unless you validate robustness thoroughly.

## Reproducibility Checklist
- [x] Training and attack setup are described with concrete hyperparameters.
- [x] Core numeric results are reported across multiple seeds.
- [ ] Official implementation repository is linked.
- [x] Hardware/runtime details are provided for efficiency benchmark.

## Related Concepts
- [[Convolutional Padding]]
- [[AutoAttack]]
- [[APGD-CE]]
- [[Adversarial Training]]
- [[LayerCAM]]
- [[Adversarial Robustness]]

