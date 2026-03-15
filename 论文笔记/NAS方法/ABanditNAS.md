---
title: "ABanditNAS"
type: method
source_paper: "Anti-Bandit Neural Architecture Search for Model Defense"
source_note: "[[ABanditNAS]]"
authors: [Hanlin Chen, Baochang Zhang, Song Xue, Xuan Gong, Hong Liu, Rongrong Ji, David Doermann]
year: 2020
venue: arXiv
tags: [nas-method, robust-nas, adversarial-defense, bandit]
created: 2026-03-15
updated: 2026-03-15
---

# ABanditNAS

## One-line Summary
> ABanditNAS searches adversarially robust cells by combining LCB-based fair sampling and UCB-based operation elimination, so search remains efficient in a very large defense-oriented operation space.

## Source
- Paper: [Anti-Bandit Neural Architecture Search for Model Defense](https://arxiv.org/abs/2008.00698)
- HTML: https://arxiv.org/html/2008.00698v2
- Code: https://github.com/RunwenHu/ABanditNAS
- Paper note: [[ABanditNAS]]

## Applicable Scenarios
- Problem type: Robust NAS for image classification under adversarial attacks.
- Assumptions: Validation accuracy after short adversarial training contains enough signal to eliminate poor operations.
- Data regime: Supervised image datasets (MNIST/CIFAR-10 in paper).
- Scale / constraints: Large operation spaces where full architecture training is unaffordable.
- Why it fits: The method explicitly addresses fairness-vs-efficiency tradeoff in huge-armed operation search.

## Not a Good Fit When
- You need guaranteed global optimality rather than heuristic pruning.
- You cannot run repeated adversarial training epochs during search.
- Your domain is far from image models and proxy signals may not transfer.

## Inputs, Outputs, and Objective
- Inputs: Training/validation data, operation sets on each edge, adversarial budget `eps`, hyperparameters `K, T, lambda`.
- Outputs: Final cell structure with one remaining operation per edge.
- Objective: Find architecture with better adversarial robustness while reducing search time.
- Core assumptions: Low-performing operations after fair trials are unlikely to become optimal later.

## Method Breakdown

### Stage 1: Build Defense-Oriented Search Space
- Construct DAG cells with `M=4` intermediate nodes and `K=9` operations per edge.
- Include max/avg pool, skip, conv/sep-conv, Gabor filter, and denoising block.
- Source: Sec. 3.1, Fig. 2

### Stage 2: LCB-Based Sampling
- Compute operation score `sL` as lower confidence bound (Eq. 3).
- Convert `sL` to sampling probabilities via `softmax(-sL)` (Eq. 4).
- Source: Sec. 3.3-3.4, Eq. (2)-(4)

### Stage 3: Adversarial One-Epoch Update
- Sample one operation per edge, adversarially train one epoch, obtain validation accuracy `a`.
- Update historical operation performance with EMA-like rule (Eq. 5).
- Source: Algorithm 1 lines 8-17, Eq. (5)

### Stage 4: UCB-Based Elimination
- Every `K*T` samples, compute `sU` (Eq. 6).
- Remove the operation with minimum `sU` on each edge (Eq. 7).
- Repeat until one operation remains on each edge.
- Source: Algorithm 1 lines 18-23, Eq. (6)-(7)

## Pseudocode
```text
Algorithm: ABanditNAS
Input: training set Dtr, validation set Dval, operation sets Omega(i,j), eps, K, T, lambda
Output: final searched robust cell structure

1. Initialize operation performance m_k,0^(i,j) for each edge operation.
   Source: Algorithm 1 line 2
2. while K > 1:
   2.1 Compute LCB-style score sL(o_k^(i,j)).
       Source: Eq. (3)
   2.2 Compute sampling probability p(o_k^(i,j)) = softmax(-sL).
       Source: Eq. (4)
   2.3 Sample one operation on each edge and train adversarially for one epoch.
       Source: Algorithm 1 lines 8-15
   2.4 Get validation accuracy a and update m_k,t^(i,j).
       Source: Algorithm 1 lines 16-17, Eq. (5)
   2.5 Every K*T samples, compute sU and prune argmin sU per edge.
       Source: Algorithm 1 lines 18-23, Eq. (6)-(7)
3. Return remaining operations as searched architecture.
   Source: Algorithm 1 output description
```

## Training Pipeline
1. Search phase:
   sample operations by anti-bandit rule and run adversarial training updates.
2. Final architecture extraction:
   keep one operation per edge after iterative pruning.
3. Final model training:
   stack searched cells and train with adversarial training settings.

Sources:
- Sec. 3.4, Algorithm 1, Sec. 4.1

## Inference Pipeline
1. Load the searched architecture.
2. Evaluate robustness under white-box and black-box attacks.
3. Report clean and adversarial accuracies.

Sources:
- Sec. 4.1-4.2, Table 1-3

## Complexity and Efficiency
- Time complexity: `O(TK^2)` (paper derivation).
- Space complexity: Not reported in closed form.
- Runtime characteristics: Search reported around 1.93h (MNIST) / 1.94h (CIFAR-10) on one Titan V.
- Scaling notes: Search space starts huge (example `9^60`), then shrinks through iterative elimination.

## Implementation Notes
- Local code path: `D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense`.
- Defense-related operations are implemented in `models/darts_ops_1.py` (`gab_filt_3x3`, `dtp_blok_3x3`).
- Archived code contains evaluation scripts and pretrained structures (e.g., `defenses/defense_all.py`, `utils/genotypes_all.py`).
- The full anti-bandit search loop from Algorithm 1 is not clearly exposed as a standalone public training script in this archive.
- Practical implication: paper logic is clear, but end-to-end search reproducibility from the provided repo is partial.

## Comparison to Related Methods
- Compared with UCBNAS: ABanditNAS adds LCB-based fairness before pruning, reducing premature elimination.
- Compared with manual architectures (LeNet/Wide-ResNet): better adversarial performance at much smaller search cost.
- Main advantage: efficient robust architecture search in a large operation space.
- Main tradeoff: relies on heuristic confidence-bound updates and short-horizon validation signals.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- Key table(s): Table 1, Table 2, Table 3
- Key equation(s): Eq. (1)-(8)
- Key algorithm(s): Algorithm 1

## References
- arXiv: https://arxiv.org/abs/2008.00698
- HTML: https://arxiv.org/html/2008.00698v2
- Code: https://github.com/RunwenHu/ABanditNAS
- Local implementation: D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense

