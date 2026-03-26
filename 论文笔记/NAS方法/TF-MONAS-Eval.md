---
title: "TF-MONAS-Eval"
type: method
source_paper: "Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training"
source_note: "[[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]"
authors: [Can Do, Ngoc Hoang Luong, Quan Minh Phan]
year: 2025
venue: RIVF
tags: [nas-method, evolutionary-nas, training-free-metrics, adversarial-robustness]
created: 2026-03-25
updated: 2026-03-25
---

# TF-MONAS-Eval

## One-line Summary
> A benchmark-driven evaluation pipeline that compares training-based and training-free objectives in evolutionary NAS under adversarial-training-aware robustness evaluation.

## Source
- Paper: [Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training](https://doi.org/10.1109/RIVF68649.2025.11365115)
- PDF: `D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf`
- Code: Not officially linked in the paper
- Paper note: [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]

## Applicable Scenarios
- Problem type: comparing search objectives for robust NAS under adversarial-training conditions.
- Assumptions: benchmark queries are trusted; search space is NAS-Bench-201-like tabular.
- Data regime: image classification on CIFAR-10, CIFAR-100, ImageNet16-120.
- Scale / constraints: useful when repeated adversarial training from scratch is too expensive.
- Why it fits: decouples objective design analysis from heavy retraining by querying benchmark metadata.

## Not a Good Fit When
- You need online search in a new search space without benchmark support.
- You need a brand-new NAS algorithm rather than an evaluation framework.
- You need task families beyond image classification without robust benchmark labels.

## Inputs, Outputs, and Objective
- Inputs: search space, objective choice (`Val-Acc-12` or `SynFlow`), optimizer (`GA` or `NSGA-II`), query budget.
- Outputs: selected architecture(s), clean/robust accuracies under multiple attacks, search-cost comparison.
- Objective: identify which objective+optimizer combinations discover architectures with better clean/robust trade-off after adversarial training.
- Core assumptions: benchmark signals from NAS-RobBench-201 are representative of adversarially trained behavior.

## Method Breakdown

### Stage 1: Run ENAS variants in NAS-Bench-201
- Execute four variants: `GA (Val-Acc-12)`, `GA (SynFlow)`, `NSGA-II (Val-Acc-12)`, `NSGA-II (SynFlow)`.
- Shared settings: population size 20, 3,000 evaluations, crossover 0.9, mutation `1/l`.
- Source: Sec. III-A, Fig. 3.

### Stage 2: Evaluate with adversarial-training benchmark labels
- For discovered architectures, query clean and attacked accuracies (FGSM, PGD, AutoAttack) from NAS-RobBench-201.
- Source: Sec. III-A, Sec. III-B/C.

### Stage 3: Representative selection for MONAS
- For NSGA-II outputs, rank candidates across all attack conditions and select one representative with minimum total rank.
- Source: Sec. III-A (CEC 2024 ranking rule reference).

### Stage 4: Statistical comparison and efficiency analysis
- Compare average performance over 31 runs with Student t-test (`p<0.01`).
- Compare search cost between training-based and training-free objectives.
- Source: Sec. III, Table I, Table II.

## Pseudocode
```text
Algorithm: TF-MONAS-Eval
Input: Search space A, objective set O={Val-Acc-12, SynFlow}, optimizers E={GA, NSGA-II}, budget T
Output: Comparative performance/cost report R

1. For each (optimizer e, objective o) in E x O, run ENAS on A with budget T.
   Source: Sec. III-A, Fig. 3
2. Collect discovered architecture(s) per run.
   Source: Sec. III-A
3. Query clean and adversarial accuracies from NAS-RobBench-201.
   Source: Sec. III-A, Sec. III-B/C
4. If e=NSGA-II, select a representative architecture via aggregate rank across conditions.
   Source: Sec. III-A (CEC 2024 ranking rule)
5. Repeat for 31 seeds, compute mean/std and significance tests.
   Source: Sec. III-A
6. Report best variants for SONAS and MONAS and their cost profile.
   Source: Table I, Table II, Sec. III-B/C
```

## Training Pipeline
1. Use benchmark-precomputed information for candidate scoring (`Val-Acc-12`, `SynFlow`, FLOPs).
2. Evolve population by crossover/mutation/selection.
3. Obtain selected architectures from each variant.
4. Evaluate architecture robustness under benchmark adversarial-training protocol.

Sources:
- Sec. II-A, Sec. III-A.

## Inference Pipeline
1. Choose search objective and optimizer family.
2. Run benchmark-based ENAS search.
3. Read selected architecture’s clean/robust profile.
4. Select architecture according to deployment preference (clean/robust balance).

Sources:
- Sec. III-A, Sec. III-B/C.

## Complexity and Efficiency
- Search evaluations per run: 3,000.
- Main cost contrast: training-based objective evaluations are significantly more expensive than SynFlow-based evaluations.
- Reported cost gap: `GA (Val-Acc-12)` > 11x `GA (SynFlow)`.
- No closed-form time complexity is provided.

## Implementation Notes
- This paper is an empirical study rather than a new algorithm proposal.
- Benchmark choice changes conclusions: robustness without adversarial training and robustness after adversarial training can yield different rankings.
- Highest SynFlow architecture is not always the strongest robust architecture under a specific attack.
- MONAS diversity is central to the gains of `NSGA-II (SynFlow)`.

## Comparison to Related Methods
- Compared with single-objective TF search:
- This framework shows TF objective alone may be insufficient after adversarial training.
- Compared with MONAS using training-based targets:
- `NSGA-II (SynFlow)` can be both better and cheaper in this benchmark setting.
- Main advantage: practical objective-selection guidance under robust NAS settings.
- Main tradeoff: tied to benchmark assumptions and limited algorithm family.

## Evidence and Traceability
- Key figure(s): Fig. 3, Fig. 4, Fig. 5.
- Key table(s): Table I, Table II.
- Key equation(s): Eq. (1)-(7) in background/problem setup.
- Key algorithm(s): GA and NSGA-II process description (Sec. II-A).

## References
- DOI: https://doi.org/10.1109/RIVF68649.2025.11365115
- PDF: D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf
- Code: Not officially linked
- Local implementation: Not archived
