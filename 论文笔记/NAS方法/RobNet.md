---
title: "RobNet"
type: method
source_paper: "When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks"
source_note: "[[RobNet]]"
authors: [Minghao Guo, Yuzhe Yang, Rui Xu, Ziwei Liu, Dahua Lin]
year: 2020
venue: CVPR
tags: [nas-method, robust-nas, one-shot-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# RobNet

## One-line Summary
> RobNet combines robust one-shot architecture sampling, statistical pattern mining, and FSP-guided filtering to discover adversarially robust CNN architectures.

## Source
- Paper: [When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks](https://arxiv.org/abs/1911.10695)
- HTML: https://openaccess.thecvf.com/content_CVPR_2020/html/Guo_When_NAS_Meets_Robustness_In_Search_of_Robust_Architectures_Against_CVPR_2020_paper.html
- Code: https://github.com/gmh14/RobNets
- Paper note: [[RobNet]]

## Applicable Scenarios
- Problem type: Robust neural architecture search for image classification under adversarial attacks.
- Assumptions: Candidate architectures can be sampled from a one-shot supernet and robustness is evaluated by adversarial accuracy.
- Data regime: Labeled image datasets with adversarial training.
- Scale / constraints: Useful when full retraining of many candidates is too expensive.
- Why it fits: It turns massive architecture evaluation into supernet sharing + short finetune + robust ranking.

## Not a Good Fit When
- You need guarantees outside attack-specific empirical robustness.
- Search spaces are not graph/cell-like and cannot be represented by edge operations.
- You require fully open-source search code for the whole discovery pipeline (the repo mainly provides searched architectures + training/eval).

## Inputs, Outputs, and Objective
- Inputs: Search space `G=(V,E)` with edge-level operations, adversarial training setup (`epsilon`, PGD steps), sampled architectures.
- Outputs: Robust architecture family (RobNet-small/medium/large/free) and design rules for robust topology.
- Objective: Identify architecture patterns that maximize adversarial accuracy under a fixed training protocol.
- Core assumptions: One-shot ranking with short adversarial finetune is informative for robustness comparison.

## Method Breakdown

### Stage 1: Robust One-shot Supernet Training
- Build a supernet covering all candidate edges/operations and sample one path per batch.
- Train sampled subnetwork by the min-max robust objective.
- Source: Sec. 3.1, Sec. 3.2, Eq. (1)

### Stage 2: Candidate Sampling, Finetuning, and Robustness Scoring
- Randomly sample candidate architectures from trained supernet.
- Adversarially finetune each sampled model for a few epochs, then evaluate PGD white-box adversarial accuracy.
- Source: Sec. 3.2, Fig. 3

### Stage 3: Pattern Mining in Cell-based Space
- Analyze top/bottom robust candidates and fit architecture-vs-robustness statistics.
- Derive density rule (`D`) and budget-aware direct-conv rule.
- Source: Sec. 3.3, Eq. (2), Fig. 4/5; Sec. 3.4, Fig. 6

### Stage 4: Cell-free Filtering via FSP Distance
- For larger search space, compute per-cell FSP distance between clean and adversarial samples.
- Filter high-FSP-loss architectures before expensive finetuning.
- Source: Sec. 3.5, Eq. (3), Eq. (4), Fig. 7

## Pseudocode
```text
Algorithm: RobNet-style Robust Architecture Discovery
Input: Search space S, training data D, attack config A, sample budget K
Output: Robust architecture set R*

1. Build supernet containing all candidate edge operations in S.
   Source: Sec. 3.2
2. Repeat over training batches:
   2.1 Randomly sample a subnetwork (path dropout).
       Source: Sec. 3.2
   2.2 Perform adversarial training with min-max objective.
       Source: Eq. (1)
3. Sample K candidate architectures from trained supernet.
   Source: Sec. 3.2
4. For each candidate:
   4.1 Adversarially finetune for a few epochs.
       Source: Sec. 3.2, Fig. 3
   4.2 Measure robust accuracy under PGD white-box attack.
       Source: Sec. 3.2
5. In cell-based mode, compute architecture density D and direct-conv ratios;
   retain designs matching robust trends.
   Source: Sec. 3.3, Eq. (2), Fig. 5; Sec. 3.4, Fig. 6
6. In cell-free mode, compute per-cell FSP loss between clean/adversarial inputs,
   reject high-loss candidates, then finetune survivors.
   Source: Sec. 3.5, Eq. (3), Eq. (4), Fig. 7
7. Select representative robust architectures as RobNet family.
   Source: Sec. 4.1, Table 1-3
```

## Training Pipeline
1. Define search space with edge operations (sep-conv / identity / zero and their combinations).
2. Train supernet with PGD-based adversarial objective.
3. Sample architectures and run short adversarial finetuning.
4. Rank by adversarial accuracy; mine robust topology patterns.
5. Instantiate representative RobNet variants and adversarially train/evaluate.

Sources:
- Sec. 3.2-3.5
- Sec. 4.1

## Inference Pipeline
1. Load selected RobNet architecture code.
2. Evaluate clean and adversarial accuracy using configured attack (FGSM/PGD/DeepFool/MI-FGSM in paper tables).
3. Report robust metrics under white-box and transfer-based black-box settings.

Sources:
- Sec. 4.2, 4.3
- Table 1, Table 2

## Complexity and Efficiency
- Cell-based space size: around `~10^8` candidates when `N=4` in their setup.
- Cell-free space: exponential explosion across layers (`(10^8)^L` scale, paper discussion).
- Runtime behavior: one-shot sharing plus short finetune makes large-scale robustness analysis feasible.
- Scaling note: FSP-guided filtering is introduced to reduce expensive evaluation in larger spaces.

## Implementation Notes
- Local code path: `D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks`.
- `main.py`: wraps model with `AttackPGD`; training mode sets `num_steps=7` to match paper training protocol.
- `attack.py`: iterative projected gradient update with random start and `epsilon` projection.
- `architecture_code.py`: stores searched architecture encodings for `robnet_large_v1/v2` and `robnet_free`.
- `models/basic_operations.py`: edge code `00/01/10/11` maps to zero/sepconv/identity/res-sepconv (code-level realization of multi-operation edge choices).
- Gap vs paper: repository focuses on training/evaluating discovered architectures; full search and FSP filtering pipeline is not fully released.

## Comparison to Related Methods
- Compared with plain [[One-shot NAS]] for natural accuracy: RobNet explicitly optimizes and analyzes adversarial robustness.
- Compared with hand-crafted DenseNet / ResNet families: RobNet keeps lower or comparable parameter counts while improving robust accuracy.
- Main advantage: practical architecture-level rules plus strong empirical gains.
- Main tradeoff: robustness conclusions are tied to attack settings and expensive adversarial training.

## Evidence and Traceability
- Key figure(s): Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6, Fig. 7
- Key table(s): Table 1, Table 2, Table 3, Table 4
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (4)
- Key algorithm(s): Robust search pseudocode in Appendix (described in Sec. 3.2)

## References
- arXiv: https://arxiv.org/abs/1911.10695
- HTML: https://openaccess.thecvf.com/content_CVPR_2020/html/Guo_When_NAS_Meets_Robustness_In_Search_of_Robust_Architectures_Against_CVPR_2020_paper.html
- Code: https://github.com/gmh14/RobNets
- Local implementation: D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks
