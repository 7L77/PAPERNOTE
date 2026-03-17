---
title: "NADR-Dataset"
type: method
source_paper: "Neural Architecture Design and Robustness: A Dataset"
source_note: "[[NADR-Dataset]]"
authors: [Steffen Jung, Jovita Lukasik, Margret Keuper]
year: 2023
venue: ICLR
tags: [nas-method, robustness-dataset, benchmark, adversarial-robustness]
created: 2026-03-17
updated: 2026-03-17
---

# NADR-Dataset

## One-line Summary

> NADR-Dataset turns NAS-Bench-201 into a robustness benchmark by exhaustively evaluating all non-isomorphic architectures on adversarial attacks and common corruptions, and storing queryable results as structured JSON artifacts.

## Source

- Paper: [Neural Architecture Design and Robustness: A Dataset](https://openreview.net/forum?id=p8coElqiSDw)
- HTML: http://robustness.vision/
- Code: https://github.com/steffen-jung/robustness-dataset
- Dataset: http://data.robustness.vision/
- Paper note: [[NADR-Dataset]]

## Applicable Scenarios

- Problem type: Offline benchmarking for robust NAS and proxy evaluation.
- Assumptions: A fixed, fully evaluated search space is acceptable for analysis and method comparison.
- Data regime: Pretrained NAS-Bench-201 models with post-hoc robustness evaluation.
- Scale / constraints: Best for methods that need many architecture-score pairs without retraining each candidate.
- Why it fits: It decouples expensive robustness evaluation from downstream algorithm iteration.

## Not a Good Fit When

- You need on-the-fly architecture training in a new search space.
- You need robustness beyond the provided attacks/corruptions or beyond NAS-Bench-201.
- You require end-to-end training logs rather than finalized evaluation tensors.

## Inputs, Outputs, and Objective

- Inputs: Architecture set `A` (NAS-Bench-201), datasets `D`, attacks/corruptions `C`, pretrained checkpoints.
- Outputs: JSON files containing `accuracy`, `confidence`, and `cm` per `(dataset, key, architecture[, epsilon/severity])`.
- Objective: Build a reusable tabular benchmark for architecture robustness analysis.
- Core assumptions: Evaluating all non-isomorphic architectures with a unified protocol yields comparable robustness signals.

## Method Breakdown

### Stage 1: Enumerate and canonicalize architectures

- Start from NAS-Bench-201 cell-based space; keep 6,466 non-isomorphic architectures.
- Keep identifier mapping to handle isomorphic variants.
- Source: Sec. 3.1, Appx A.1, Fig. 8.

### Stage 2: Load pretrained checkpoints per dataset

- For each architecture and each dataset split, load released pretrained parameters.
- Evaluate on CIFAR-10, CIFAR-100, and ImageNet16-120.
- Source: Sec. 3.1, Alg. 1 (Appx A.2).

### Stage 3: Run adversarial robustness evaluations

- Evaluate FGSM, PGD, APGD-CE, and Square under multiple `epsilon` values.
- Store architecture-level accuracy, confidence, and confusion matrix outputs.
- Source: Sec. 3.2, Eq. (1)-(3), Table 2, Fig. 2-3.

### Stage 4: Run common corruption evaluations

- Evaluate CIFAR-10-C and CIFAR-100-C over 15 corruption types and 5 severities.
- Store the same output triplet (`accuracy`, `confidence`, `cm`).
- Source: Sec. 3.3, Fig. 4-5.

### Stage 5: Persist benchmark artifacts

- Save files as `{key}_{measurement}.json` under dataset folders.
- Maintain global metadata (`meta.json`) with ID mappings and epsilon grids.
- Source: Appx A.3-A.4, Table 3-4, Fig. 10-11.

## Pseudocode

```text
Algorithm: Robustness Dataset Gathering (NADR-Dataset)
Input: Architecture space A, datasets D, attacks/corruptions C, result store R
Output: Structured robustness benchmark files

1. For each architecture a in A:
   load pretrained weights for a on each dataset d.
   Source: Alg. 1, line 1-3; Sec. 3.1
2. For each dataset d in D:
   For each corruption/attack operator c in C:
      construct transformed evaluation data d_c from d.
      Source: Alg. 1, line 4-5; Sec. 3.2/3.3
3. Evaluate model a on d_c and collect:
   Accuracy, Confidence, ConfusionMatrix.
   Source: Alg. 1, line 6
4. Write outputs into nested result dictionary:
   R[d][c]["accuracy"][a], R[d][c]["confidence"][a], R[d][c]["cm"][a].
   Source: Alg. 1, line 7-9
5. Export JSON files by key and measurement; keep metadata for id/isomorph/eps.
   Source: Appx A.4, Table 3-4, Fig. 10-11
```

## Training Pipeline

1. Train architectures once via NAS-Bench-201 protocol (provided checkpoints).
2. Reuse fixed checkpoints for all robustness evaluations.
3. Execute attack/corruption sweeps and aggregate outputs.
4. Publish dataset snapshots and helper API for querying.

Sources:

- Sec. 3.1-3.3, Appx A.2-A.4.

## Inference Pipeline

1. Instantiate `RobustnessDataset(path=...)`.
2. Query by data source (`cifar10/cifar100/ImageNet16-120`), key, and measure.
3. Map architecture IDs through `get_uid()` to non-isomorphic canonical IDs when needed.
4. Use queried tensors for ranking, correlation, or search-algorithm simulation.

Sources:

- Local code: `robustness_dataset.py` (`query`, `get_uid`, `id_to_string`, `string_to_id`).
- Appx A.4, Table 4.

## Complexity and Efficiency

- Time complexity: Proportional to `|A| x |D| x |C| x eval_cost`.
- Space complexity: Proportional to stored tensors for all `(dataset, key, measure, architecture)`.
- Runtime characteristics: Collection requires cluster-scale compute due exhaustive attack/corruption sweeps.
- Scaling notes: Fixed-benchmark reuse makes downstream method development cheap after dataset construction.

## Implementation Notes

- Code-level key names include explicit norms, e.g. `pgd@Linf`, `aa_apgd-ce@Linf`.
- `query(..., missing_ok=True)` can skip absent files and still return partial results.
- For `ImageNet16-120`, common corruption keys are skipped by design in helper logic.
- `meta.json` stores isomorphic mapping; consumers should canonicalize IDs before analysis.
- Paper-code gap: the public repo focuses on dataset access; full data-generation cluster scripts are not fully exposed.

## Comparison to Related Methods

- Compared with [[NAS-Bench-201]]: adds robustness dimensions (attacks/corruptions) beyond clean accuracy.
- Compared with [[RobustBench]]: architecture-space exhaustive evaluation rather than leaderboard model comparison.
- Main advantage: enables reproducible robust-NAS experiments without retraining every candidate.
- Main tradeoff: benchmark scope is bounded by one search space and predefined attack/corruption settings.

## Evidence and Traceability

- Key figure(s): Fig. 1-7, Fig. 9-11.
- Key table(s): Table 1-4.
- Key equation(s): Eq. (1)-(4).
- Key algorithm(s): Algorithm 1 (Appx A.2).

## References

- OpenReview: https://openreview.net/forum?id=p8coElqiSDw
- Project: http://robustness.vision/
- Code: https://github.com/steffen-jung/robustness-dataset
- Dataset: http://data.robustness.vision/
- Local implementation: D:/PRO/essays/code_depots/Neural architecture design and robustness a dataset

