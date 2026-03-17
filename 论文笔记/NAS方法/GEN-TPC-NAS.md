---
title: "GEN-TPC-NAS"
type: method
source_paper: "Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers"
source_note: "[[GEN-TPC-NAS]]"
authors: [Jun-Hua Ko, Tzi-Dar Chiueh]
year: 2025
venue: IJCNN
tags: [nas-method, zero-shot-nas, self-supervised-learning, transformer]
created: 2026-03-17
updated: 2026-03-17
---

# GEN-TPC-NAS

## One-line Summary

> GEN-TPC-NAS is a two-stage zero-shot evolutionary search that first filters Transformer architectures by TPC expressivity, then switches to entropy-based SSL generalization scoring under a TPC floor.

## Source

- Paper: [Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers](https://doi.org/10.1109/IJCNN64981.2025.11229357)
- HTML: https://ieeexplore.ieee.org/document/11229357
- Code: Not reported in the paper
- Paper note: [[GEN-TPC-NAS]]

## Applicable Scenarios

- Problem type: Zero-shot Transformer architecture search for CV/NLP under limited labels.
- Assumptions: TPC approximates expressivity and feature-spectrum entropy approximates generalization potential.
- Data regime: Unlabeled pre-training + low-labeled fine-tuning settings.
- Scale / constraints: Best when architecture evaluation by full training is too expensive.
- Why it fits: It preserves fast zero-shot search while explicitly balancing expressivity and generalization.

## Not a Good Fit When

- You need fully code-verified implementation details beyond paper-level algorithm description.
- The target architecture family is far from Transformer block assumptions used in Eq. (5).
- Proxy reliability is weak in your domain due different initialization/data statistics.

## Inputs, Outputs, and Objective

- Inputs: Search space S (Embed/QKV/Head/MLP ratio), constraints K (FLOPs/Params/depth), population size N, iterations M, threshold T0.
- Outputs: Best architecture Fmax and its proxy scores (TPC, Entropy).
- Objective: Find architecture maximizing performance under constraints by balancing expressivity and generalization proxy signals.
- Core assumptions: High TPC is needed but insufficient; high entropy under adequate TPC better predicts low-label transfer behavior.

## Method Breakdown

### Stage 1: TPC-guided Exploration

- Initialize population and generate candidates via mutation/crossover.
- Evaluate with TPC score St and keep top-N by St.
- Source: Sec. III-C, Alg. 1 (lines 1-18), Eq. (6).

### Stage 2: Switch Trigger by TPC Convergence

- Monitor St(Fmax) - St(Fmin) in current population.
- When difference <= T0, set TPCThreshold=St(Fmin) and switch to entropy scoring.
- Source: Sec. III-C, Alg. 1 (lines 29-31).

### Stage 3: Entropy-guided Exploitation under TPC Floor

- Reject candidates with St <= TPCThreshold.
- For remaining candidates, compute entropy score Se and rank by Se.
- Source: Sec. III-C, Alg. 1 (lines 19-24), Eq. (1)-(2).

### Stage 4: Final Selection and SSL Training

- Return architecture with highest current score in final population.
- Pre-train in SSL setup, then fine-tune in standard/low-label settings.
- Source: Sec. III-C (search), Sec. IV-A/B (training and evaluation).

## Pseudocode

```text
Algorithm: GEN-TPC-NAS
Input: Search space S, constraints K, max depth D, iterations M, population size N, threshold T0
Output: Best architecture Fmax

1. Initialize population P with N random architectures.
   Source: Alg. 1, lines 1-4
2. Generate candidate F_hat via mutation or crossover, then enforce K and D constraints.
   Source: Alg. 1, lines 5-13
3. Compute TPC score St(F_hat) and insert candidate.
   Source: Alg. 1, lines 14-18, Eq. (6)
4. If switchFlag is False and St(Fmax)-St(Fmin) <= T0:
      set TPCThreshold = St(Fmin), switchFlag = True.
   Source: Alg. 1, lines 29-31
5. If switchFlag is True:
      keep candidate only when St(F_hat) > TPCThreshold,
      then compute entropy score Se(F_hat) and rank by Se.
   Source: Alg. 1, lines 19-24; Eq. (1)-(2)
6. Maintain population size N by removing lowest-score individual.
   Source: Alg. 1, line 28
7. Return Fmax after M iterations.
   Source: Alg. 1, line 33
```

## Training Pipeline

1. Run GEN-TPC-NAS search in target search space with fixed constraints.
2. Select searched architecture (e.g., GEN-TPC-Tiny / GEN-TPC-GPT2).
3. Pre-train using SSL objective (MIM for ViT, autoregressive LM for GPT2).
4. Fine-tune for full-label and low-label downstream evaluation.

Sources:

- Sec. III-C, Sec. IV-A, Table III.

## Inference Pipeline

1. For a new search run, evaluate candidates by TPC first.
2. Switch to entropy phase when TPC diversity in population collapses.
3. Output best architecture and deploy with standard inference of chosen backbone.

Sources:

- Sec. III-C, Alg. 1.

## Complexity and Efficiency

- Time complexity: Not reported as closed-form.
- Space complexity: Not reported as closed-form.
- Runtime characteristics: Search cost reported as 0.02 GPU-days on ImageNet-1K setup.
- Scaling notes: Proxy computation avoids full training during search; downstream pre-train/fine-tune remains dominant cost.

## Implementation Notes

- Search hyperparameters (reported): population size 100, 1000 generations, T0=0.5.
- Constraint handling is hard-filter style before score insertion.
- Transformer search knobs: embed dim, QKV dim, head dim, MLP ratio.
- Entropy score uses per-head feature matrix spectrum; SVD and normalized eigenvalue entropy are core.
- If T0 too small (e.g., 0), method degenerates toward TPC-only behavior; if too large, may over-prioritize entropy.

## Comparison to Related Methods

- Compared with [[TPC-NAS]]: adds generalization-aware entropy stage and switching logic.
- Compared with [[MaskTAS]]: keeps SSL but uses zero-shot proxy search instead of one-shot supernet training.
- Main advantage: strong low-label performance with very low search budget.
- Main tradeoff: depends on proxy validity; no official code link in paper to verify all implementation details.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 5, Fig. 6, Fig. 7, Fig. 8.
- Key table(s): Table I-IX (especially IV, VI, VIII, IX).
- Key equation(s): Eq. (1)-(6).
- Key algorithm(s): Algorithm 1.

## References

- DOI: https://doi.org/10.1109/IJCNN64981.2025.11229357
- HTML: https://ieeexplore.ieee.org/document/11229357
- Code: Not reported in the paper
- Local implementation: Not archived (no official repository link found in paper)

